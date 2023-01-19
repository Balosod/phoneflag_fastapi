from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import BaseModel, EmailStr, Field,validator
from datetime import date
from enum import Enum

today = date.today()

class account_type(str,Enum):
    personal_account = "personal"
    cooperate_account = "cooperate"
    
class User(Document):
    firstname: str
    lastname: str
    email: EmailStr
    phone:str
    password: str
    account:Optional[account_type] = None
    is_admin:bool = False
    is_affiliate:bool = False
    created:str = today.strftime("%B %d, %Y")
    active: bool = False
    
    @validator('password', always=True)
    def validate_password(cls, password):
        
        min_length = 8
        errors = ''
        if len(password) < min_length:
            errors += 'Password must be at least 8 characters long. '
        if not any(character.islower() for character in password):
            errors += 'Password should contain at least one lowercase character.'
        if errors:
            raise ValueError(errors)
            
        return password
    

    class Settings:
        name = "users"

    


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example" : {
                "email": "johndoe@mail.com",
                "password": "yoursecretpa55word",
            }
        }

class OtpSchema(BaseModel):
    email: EmailStr = Field(...)
    otp: str = Field(...)
    
    
class EmailSchema(BaseModel):
    email: EmailStr = Field(...)
    

def SuccessResponseModel(data, code, message):
    return { "data": [data], "code": code, "message": message }


def ErrorResponseModel(error, code, message):
    return { "error": error, "code": code, "message": message }