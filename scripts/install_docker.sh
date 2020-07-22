#!/bin/bash

# Script for installing docker on Ubuntu

sudo apt-get update -yqq
sudo apt-get -yqq install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt-get update
apt-cache policy docker-ce
sudo apt-get -yqq install docker-ce
sudo systemctl enable docker
sudo systemctl status docker
sudo groupadd docker
sudo usermod -aG docker $USER
