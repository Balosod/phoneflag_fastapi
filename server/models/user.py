from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import BaseModel, EmailStr, Field,validator
from enum import Enum



class Gender(str,Enum):
    male = "male"
    female = "female"
    other = "other"
    
class User(Document):
    username: Optional[str] = None
    full_name: Optional[str] = None
    address:Optional[str] = None
    date_of_birth:Optional[str] = None
    phone:Optional[str] = None
    email: EmailStr
    sales:Optional[int] = 0
    boughts:Optional[int] = 0
    gender:Optional[Gender] = None
    store_name:Optional[str] = None
    img:Optional[str]
    password: str
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

    

class RegistrationSchema(BaseModel):
    username: Optional[str] = None
    email: EmailStr
    password: str
   
    
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
    

class ImageSchema(BaseModel):
    image: str
    
class ProfileDataSchema(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    store_name: Optional[str] = None
    phone:Optional[str] = None
    address:Optional[str] = None
    
   
class PasswordSchema(BaseModel):
    current_password: str
    new_password:str
    
    
    

def SuccessResponseModel(data, code, message):
    return { "data": [data], "code": code, "message": message }


def ErrorResponseModel(error, code, message):
    return { "error": error, "code": code, "message": message }