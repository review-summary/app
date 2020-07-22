
## Requirements

First, you need to install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html),
[Docker](https://docs.docker.com/get-docker/) (on Ubuntu linux, you can use the `scripts/install_ubuntu.sh`
script), and [Terraform](https://learn.hashicorp.com/terraform/getting-started/install.html).

## Setup infrastructure

Before starting, export the AWS credentials ([AWS IAM](https://console.aws.amazon.com/iam/))
to environment variables (hint: you can add them to `.bashrc`).

```bash
export AWS_ACCOUNT_ID="account_id"
export AWS_ACCESS_KEY_ID="anaccess_key"
export AWS_SECRET_ACCESS_KEY="secret_key"
export AWS_DEFAULT_REGION="us-west-2"  # example
```

To setup infrastructure, first create SSH keys with `make keys`, then run Terraform

```bash
terraform init
terraform apply
```

Terraform will setup virtual machine on [AWS EC2](https://console.aws.amazon.com/ec2).
To login into the machine, run

```bash
ssh -i key ubuntu@<ip address of the machine>
```

Finally, when you want to turn it off, run `terraform destroy` and it will cleanup everything for you.
