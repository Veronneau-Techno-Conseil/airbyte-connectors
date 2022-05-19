#!/bin/sh

sudo apt-get update 

sudo apt-get install ca-certificates curl gnupg lsb-release 

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-compose -y

sudo docker run hello-world

sudo service docker start

mkdir airbyte && cd airbyte
wget "https://raw.githubusercontent.com/airbytehq/airbyte/master/.env"
wget "https://raw.githubusercontent.com/airbytehq/airbyte/master/docker-compose.yaml"
sudo docker-compose up -d
