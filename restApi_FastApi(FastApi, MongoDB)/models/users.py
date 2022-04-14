# обьявление типов для моделей 23:55

from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str]
    name: str
    email: str
    password: str


