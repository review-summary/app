#!/bin/bash
set -e

sudo apt-get update -yqq
sudo apt-get -yqq install apt-transport-https ca-certificates curl software-properties-common unzip

# Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt-get update -yqq
apt-cache policy docker-ce
sudo apt-get -yqq install docker-ce
sudo systemctl enable docker
sudo systemctl status docker
# sudo groupadd docker
sudo usermod -aG docker $USER

# AWS CLI
curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -qq awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip
