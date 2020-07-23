# Script reads the AWS_ACCOUNT_ID and AWS_DEFAULT_REGION enviroment variables

ECR_URL ?= ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com
REPOSITORY ?= ws-capstone
TAG ?= 0.1
IMAGE ?= $(ECR_URL)/$(REPOSITORY):$(TAG)

.PHONY: build-docker infrastructure setup-aws run push auth clean help
.DEFAULT_GOAL := help

build: auth build-docker push infra setup-aws

build-docker: ## Build docker
	docker build --rm -t $(IMAGE) -f Dockerfile .

infra: ## Setup AWS infrastructure
	terraform apply -auto-approve

setup-aws: ## Setup AWS EC2 instance
	@ $(eval IP=$(shell aws ec2 describe-instances --filter Name=tag:Name,Values=ws-capstone \
		--query 'Reservations[].Instances[].PublicIpAddress' --output text))
	ssh -o "StrictHostKeyChecking no" -i key ubuntu@$(IP) < scripts/setup_instance.sh
	ssh -o "StrictHostKeyChecking no" -i key ubuntu@$(IP) "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} \
		| docker login --username AWS --password-stdin $(ECR_URL) \
		&& docker run --rm $(IMAGE)"

run: ## Run docker image
	docker run --rm $(IMAGE)

push: ## Push docker image to remote repository
	# For details see:
	# https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth
	# https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html
	# https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html

	aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin $(ECR_URL)
	aws ecr create-repository --repository-name $(REPOSITORY) || true 2>/dev/null
	docker push $(IMAGE)
	@ docker logout

auth: ## Generate SSH keypair
	@ rm -rf key*
	ssh-keygen -t rsa -f key -q -N ""
	@ chmod 400 key*

clean: ## Shutdown AWS and cleanup the working files
	terraform destroy -auto-approve
	rm -rf terraform.tfstate *.backup key*

help: ## Display this help
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
