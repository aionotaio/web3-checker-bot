from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_host: str = "mongodb"
    mongo_port: int = 27017
    mongo_initdb_root_username: str
    mongo_initdb_root_password: str
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    bot_api_token: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_seconds: int = 3600


settings = Settings()
