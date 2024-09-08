from pydantic import BaseModel


class Config(BaseModel):
    minecraft_token: str = 'DefaultToken'
