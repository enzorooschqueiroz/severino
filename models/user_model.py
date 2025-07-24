#models/user_model.py
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password_hash: Annotated[str, Field(min_length=6)]
