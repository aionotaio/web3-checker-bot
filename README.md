# Web3 Checker Bot + Admin Panel

## About
- Telegram bot that checks allocations and eligibility for Sophon, Space and Time, 0G Node, and Jager airdrops
- Admin Panel that allows to manage bot more effectively

## Used tech stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-1E90FF?style=for-the-badge&logo=Telegram&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=RabbitMQ&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![aiohttp](https://img.shields.io/badge/aiohttp-2C5BB4?style=for-the-badge&logo=aiohttp&logoColor=white)
![Jinja2](https://img.shields.io/badge/jinja2-7E0C1B?style=for-the-badge&logo=jinja&logoColor=white)

### Follow: https://t.me/touchingcode

## Quick Start
- Initialize environment variables in the `.env.example` file and rename it just to `.env`

- Download Docker

- Use command below to start bot and admin panel:
```
docker compose up -d --build
```

- Use command below to start ONLY bot:
```
docker compose up -d --build bot
```

> To login into admin panel you first need to create an admin using a command below
```
docker exec -it admin-panel python scripts/create_admin.py
```

## Environment variables
|Name|Description|
|---|---|
|MONGO_HOST|MongoDB hostname (default is `mongodb`)|
|MONGO_PORT|MongoDB port (default is `27017`)|
|MONGO_INITDB_ROOT_USERNAME|MongoDB username|
|MONGO_INITDB_ROOT_PASSWORD|MongoDB password|
|RABBITMQ_HOST|RabbitMQ hostname (default is `rabbitmq`)|
|RABBITMQ_PORT|RabbitMQ port (default is `5672`)|
|RABBITMQ_DEFAULT_USER|RabbitMQ username|
|RABBITMQ_DEFAULT_PASS|RabbitMQ password|
|BOT_API_TOKEN|Your Telegram Bot API token|
|JWT_SECRET_KEY|JWT secret key|
|JWT_ALGORITHM|JWT algorithm (default is `HS256`)|
|JWT_EXPIRE_SECONDS|JWT token expiration time in seconds (default is `3600`) |

## Possible questions
- What is `JWT_SECRET_KEY` and where can I get it?

> JWT Secret Key is used for signing and authentication of JWT tokens (JSON Web Token). For example you can generate it using node.js command like this: `node -e "console.log(require('crypto').randomBytes(32).toString('hex'));"`

> ...or just pass any other value, but it needs to be a secret only you know :)

## Deployment guide on any Linux Ubuntu server
- Use commands below:
```
sudo apt update
sudo apt install curl software-properties-common ca-certificates apt-transport-https -y
wget -O- https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor | sudo tee /etc/apt/keyrings/docker.gpg > /dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce -y
sudo apt-get install docker-compose
cd <project_dir>
docker compose up -d --build
// or 
docker compose up -d --build bot
```