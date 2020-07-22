# Script reads the AWS_ACCOUNT_ID and AWS_DEFAULT_REGION enviroment variables

ECR_URL ?= ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com
REPOSITORY ?= ws-capstone
TAG ?= 0.1
IMAGE ?= $(ECR_URL)/$(REPOSITORY):$(TAG)

.PHONY: build-docker setup-instance run push auth clean help
.DEFAULT_GOAL := help

build: auth build-docker push setup-instance

build-docker: ## Build docker
	docker build --rm -t $(IMAGE) -f Dockerfile .

setup-instance: ## Setup AWS EC2 instance
	@ terraform apply
	@ $(eval IP=$(shell aws ec2 describe-instances --filter Name=tag:Name,Values=ws-capstone \
		--query 'Reservations[].Instances[].PublicIpAddress' --output text))
	@ ssh -i key ubuntu@$(IP) < scripts/setup_instance.sh
	@ scp -q ecr_pass ubuntu@$(IP):/home/ubuntu/
	@ ssh -i key ubuntu@$(IP) "cat ecr_pass | docker login --username AWS --password-stdin $(ECR_URL) \
		&& docker run --rm $(IMAGE)"

run: ## Run docker image
	docker run --rm $(IMAGE)

push: ## Push docker image to remote repository
	# For details see:
	# https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth
	# https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html
	# https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html

	@ cat ecr_pass | docker login --username AWS --password-stdin $(ECR_URL)
	@ aws ecr create-repository --repository-name $(REPOSITORY) || true 2>/dev/null
	docker push $(IMAGE)
	@ docker logout

auth: ## Generate SSH keypair
	@ rm -rf key* ecr_pass
	@ ssh-keygen -t rsa -f key
	@ chmod 400 key*
	@ aws ecr get-login-password --region ${AWS_DEFAULT_REGION} > ecr_pass

clean: ## Cleanup the working files
	@ rm -rf .terraform terraform.tfstate *.backup

help: ## Display this help
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
