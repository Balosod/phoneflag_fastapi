from typing import Optional, List
from beanie import Document,PydanticObjectId, Link
from pydantic import BaseModel, EmailStr, Field,validator
from enum import Enum

from datetime import date

today = date.today()


class Status(str,Enum):
    tracking = "tracking"
    requested = "requested"

class Tracking(Document):
    tracking_id:Optional[str]
    device_model:str
    imel_number:str
    device_condition:str
    device_id_num:Optional[str]
    last_backup:str
    email:EmailStr
    date_of_request:str = today.strftime("%d %b %Y")
    status:Status=Status.requested
    owner_id: PydanticObjectId
    
    class Settings:
        name = "tracking"
        
        
class TrackingSchema(BaseModel):
    device_model:str
    imel_number:str
    device_condition:str
    last_backup:str
    email:EmailStr
    