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
