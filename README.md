
## Requirements

First, you need to install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html),
[Docker](https://docs.docker.com/get-docker/), and [Terraform](https://learn.hashicorp.com/terraform/getting-started/install.html). Next, go to the main folder of the repo and run `terraform init` to download the aws
plugin for Terraform.

## Run the container locally

To build the container run `make docker`, and to run it locally use `make run`.

## Run the container on AWS EC3

Before starting, export the [AWS credentials](https://console.aws.amazon.com/iam/)) to environment
variables (hint: you can add them to `.bashrc`).

```bash
export AWS_ACCOUNT_ID="account_id"
export AWS_ACCESS_KEY_ID="anaccess_key"
export AWS_SECRET_ACCESS_KEY="secret_key"
export AWS_DEFAULT_REGION="us-west-2"  # example
```

To setup infrastructure just run `make build` and `make setup-aws`. The command will build the
Docker image, push it to [ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html),
setup AWS infrastructure, install AWS CLI and Docker on the [EC2](https://console.aws.amazon.com/ec2)
machine, and run the Docker image on it. If you want to connect to the EC2 instance, just run
`make connect` and it will connect you via SSH.

## Turn-off the AWS EC2 instance and clean working files

Finally, when you want to turn it off, run `make clean` and it will turn off the infrastructure
(run `terraform destroy`) and cleanup everything for you.
