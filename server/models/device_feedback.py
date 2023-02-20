from typing import Optional, List
from beanie import Document,PydanticObjectId, Link
from pydantic import BaseModel, EmailStr, Field,validator
from enum import Enum



   
class Ratings(str,Enum):
    _1 = "1"
    _2 = "2"
    _3 = "3"
    _4 = "4"
    _5 = "5"
     
     
    
    
class DeviceFeedback(Document):
    rating:Optional[Ratings] = None
    name:str
    review:Optional[str] = None
    liked:Optional[int] = 0
    owner_id:PydanticObjectId
    device_id:PydanticObjectId
    replys:Optional[list] = []
    
    
    class Settings:
        name = "devices_feedback"
    
    
     
class ReplySchema(BaseModel):
    reply:str
    review_id:PydanticObjectId
    
     
class LikeSchema(BaseModel):
    review_id:PydanticObjectId
    
    
    
class ReviewSchema(BaseModel):
    review:Optional[str] = None
    device_id:PydanticObjectId
    
    
   
class RatingSchema(BaseModel):
    rating:Optional[Ratings] = None
    device_id:PydanticObjectId
    
    

 
    