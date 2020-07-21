.PHONY: keys clean help
.DEFAULT_GOAL := help

keys: ## Generate SSH keypair
	@ ssh-keygen -t rsa -f key
	@ chmod 400 key*

clean: ## Cleanup the working files
	@ rm -rf .terraform terraform.tfstate *.backup
	@ rm -rf key*

help: ## Display this help
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
