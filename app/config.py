from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_hostname_testing: str
    database_port: str
    database_password: str
    database_name_testing: str
    database_name: str
    database_username: str
    database_port_testing: str
    secret_key: str
    algorithm: str
    token_expiry: int
    smtp_mail: str
    smtp_password: str

    class Config:
        env_file = ".env"


settings = Settings()
