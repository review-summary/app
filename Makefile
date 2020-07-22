# Script reads the AWS_ACCOUNT_ID and AWS_DEFAULT_REGION enviroment variables

ECR_URL ?= ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com
REPOSITORY ?= ws-capstone
TAG ?= 0.1
IMAGE ?= $(ECR_URL)/$(REPOSITORY):$(TAG)

.PHONY: build run push keys clean help
.DEFAULT_GOAL := help

build: ## Build docker
	docker build --rm -t $(IMAGE) -f Dockerfile .

run: ## Run docker image
	docker run --rm $(IMAGE)

push: ## Push docker image to remote repository
	# For details see:
	# https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth
	# https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html
	# https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html

	@ bash scripts/ecr_pass.sh | docker login --username AWS --password-stdin $(ECR_URL)
	@ aws ecr create-repository --repository-name $(REPOSITORY) || true 2>/dev/null
	docker push $(IMAGE)
	@ docker logout

keys: ## Generate SSH keypair
	@ ssh-keygen -t rsa -f key
	@ chmod 400 key*

clean: ## Cleanup the working files
	@ rm -rf .terraform terraform.tfstate *.backup
	@ rm -rf key*

help: ## Display this help
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
