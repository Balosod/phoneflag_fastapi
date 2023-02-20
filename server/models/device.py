from typing import Optional, List
from beanie import Document,PydanticObjectId, Link
from pydantic import BaseModel, EmailStr, Field,validator
from enum import Enum


class DeviceImage(Document):
    img:str
    
    class Settings:
        name = "device_image"
        
        
class Category(str,Enum):
    handphone = "handphone"
    tablet = "tablet"
    laptop = "laptop"
    computer = "computer"
    television = "television"
    
class Brand(str,Enum):
    apple = "apple"
    xiaomi = "xiaomi"
    samsung = "samsung"
    asus = "asus"
    realme = "realme"
    huawel = "huawel"
    
    
class FirstCondition(str,Enum):
    brand_new = "brand_new"
    second = "second"
    
class InternalStorage(str,Enum):
    _16GB = "16GB"
    _32GB = "32GB"
    _64GB = "64GB"
    _128GB = "128GB"
    _256GB = "256GB"
    _512GB = "512GB"

class OperatingSystem(str,Enum):
    andriod = "andriod"
    apple_ios = "apple_ios"

class Device(Document):
    name:str
    category:Category = None
    brand:Brand = None
    first_condition:FirstCondition = None
    second_condition:str
    internal_storage:InternalStorage = None
    screen_size:str
    battery_capacity:str
    operating_system:OperatingSystem = None
    weight:str
    color:str
    description:str
    location:str
    discount_price:int
    off_price:int
    times_bought:Optional[int]=0
    minimum_order:int = 0
    sponsored:bool = False
    todays_deal:bool = False
    best_sellers:bool = False
    images:Optional[List[Link[DeviceImage]]] = None
    owner_id: PydanticObjectId
    
    class Settings:
        name = "devices"
        
        
        

class DeviceSchema(BaseModel):
    name:str
    category:Category = None
    brand:Brand = None
    first_condition:FirstCondition = None
    second_condition:str
    internal_storage:InternalStorage = None
    screen_size:str
    battery_capacity:str
    operating_system:OperatingSystem = None
    weight:str
    color:str
    description:str
    location:str
    minimum_order:int
    discount_price:int
    off_price:int
    images:Optional[list] = None
   
    