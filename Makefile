# Script reads the AWS_ACCOUNT_ID and AWS_DEFAULT_REGION enviroment variables

SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c 
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

ECR_URL ?= ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com
REPOSITORY ?= ws-capstone
TAG ?= 0.1
IMAGE ?= $(ECR_URL)/$(REPOSITORY):$(TAG)

# IP address of the EC2 instance
IP ?= $(shell aws ec2 describe-instances --filter Name=tag:Name,Values=ws-capstone \
		--query 'Reservations[].Instances[].PublicIpAddress' --output text)

.DEFAULT_GOAL := help 
.PHONY: docker setup-aws run push clean connect test help

build: key key.pub docker push terraform.tfstate

docker: ## Build docker
	docker build --rm -t $(IMAGE) -f Dockerfile .

run: ## Run docker image
	docker run -p 5000:5000 --rm $(IMAGE)

test: docker ## Run docker image
	docker run --rm $(IMAGE) pytest /app/tests

push: ## Push docker image to remote repository
	# For details see:
	# https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth
	# https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html
	# https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html

	aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin $(ECR_URL)
	aws ecr create-repository --repository-name $(REPOSITORY) || true 2>/dev/null
	docker push $(IMAGE)
	@ docker logout

.terraform:
	terraform init

terraform.tfstate: .terraform ## Setup AWS infrastructure
	terraform apply -auto-approve

setup-aws: ## Setup AWS EC2 instance and start the docker
	@ sleep 3
	ssh -i key ubuntu@$(IP) < scripts/setup_instance.sh
	ssh -i key ubuntu@$(IP) "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} \
		| docker login --username AWS --password-stdin $(ECR_URL) \
		&& docker run -p 5000:5000 --rm $(IMAGE)"

key: ## Generate SSH keypair
	ssh-keygen -t rsa -f key -q -N ""
	@ chmod 400 key*

key.pub: key

clean: ## Shutdown AWS and cleanup the working files
	terraform destroy -auto-approve
	rm -rf terraform.tfstate *.backup key*

connect: ## Connect to EC2 instance via SSH
ifeq "$(IP)" ""
	$(error unknown IP address)
endif
	ssh -o StrictHostKeyChecking=accept-new -i key ubuntu@$(IP)

help: ## Display this help
	@ grep -E '^[a-zA-Z_-.]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
