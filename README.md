# Web3 Checker Bot

## About
- Telegram bot that checks allocations and eligibility for Sophon, Space and Time, 0G Node, and Jager airdrops

## Used tech stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=RabbitMQ&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-1E90FF?style=for-the-badge&logo=Telegram&logoColor=white)
![aiohttp](https://img.shields.io/badge/aiohttp-2C5BB4?style=for-the-badge&logo=aiohttp&logoColor=white)

### Follow: https://t.me/touchingcode

## Quick Start
- Initialize environment variables in the `.env.example` file and rename it just to `.env`

- Download and start Docker Desktop from the official website

- Use commands: \
`docker compose build` \
`docker compose up -d` 

## Deployment guide on any Linux Ubuntu server
- Use commands: \
`sudo apt update` \
`sudo apt install curl software-properties-common ca-certificates apt-transport-https -y` \
`wget -O- https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor | sudo tee /etc/apt/keyrings/docker.gpg > /dev/null` \
`echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null` \
`sudo apt update` \
`sudo apt install docker-ce -y` \
`sudo apt-get install docker-compose` \
`cd <project_dir>` \
`docker compose build` \
`docker compose up -d` 