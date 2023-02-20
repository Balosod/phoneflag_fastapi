from typing import Optional, List
from beanie import Document,PydanticObjectId, Link
from pydantic import BaseModel, EmailStr, Field,validator
from enum import Enum


class Order(Document):
    device_id: PydanticObjectId
    owner_id: PydanticObjectId
    
    class Settings:
        name = "orders"
        
        
class OrderSechema(BaseModel):
    device_id: PydanticObjectId