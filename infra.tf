# For details see:
# https://www.terraform.io/docs/providers/aws/index.html
# https://dev.to/aakatev/deploy-ec2-instance-in-minutes-with-terraform-ip2

# Read the configuration from enviroment variables:
# $ export AWS_ACCESS_KEY_ID="anaccesskey"
# $ export AWS_SECRET_ACCESS_KEY="asecretkey"
# $ export AWS_DEFAULT_REGION="us-west-2"

provider "aws" {}

# Use local ssh keys 'key' and 'key.pub'
resource "aws_key_pair" "web" {
  key_name   = "web"
  public_key = file("key.pub")
}

# see: https://www.terraform.io/docs/providers/aws/r/iam_role_policy.html
resource "aws_iam_role" "ec2_role" {
  name               = "ec2_role"
  assume_role_policy = file("iam_role_ec2.json")
}

# see: https://console.aws.amazon.com/iam
resource "aws_iam_policy" "ecr_s3_access" {
  name   = "ecr_s3_access"
  policy = file("iam_policy_ecr_s3.json")
}

resource "aws_iam_role_policy_attachment" "role_policy_attachment" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.ecr_s3_access.arn
}

resource "aws_iam_instance_profile" "iam_instance_profile" {
  name = "iam_instance_profile"
  role = aws_iam_role.ec2_role.name
}

resource "aws_security_group" "web" {
  name        = "allow-ssh"
  description = "Allow SSH traffic"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_all"
  }
}

resource "aws_instance" "web" {
  key_name      = aws_key_pair.web.key_name
  ami           = "ami-0d359437d1756caa8"
  instance_type = "t2.micro"

  tags = {
      Name = "ws-capstone"
  }

  iam_instance_profile = aws_iam_instance_profile.iam_instance_profile.name

  vpc_security_group_ids = [
      aws_security_group.web.id
  ]

  connection {
      type        = "ssh"
      user        = "web"
      private_key = file("key")
      host        = self.public_ip
  }
}
