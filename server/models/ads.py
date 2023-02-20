from typing import Optional, List
from beanie import Document,PydanticObjectId, Link
from pydantic import BaseModel, EmailStr, Field,validator
from enum import Enum

class AdsStatus(str,Enum):
    approve = "approve"
    on_review = "on_review"

class AdsImages(Document):
    img:str
    
    class Settings:
        name = "ads_image"
        
        
class AdsVideos(Document):
    img:str
    
    class Settings:
        name = "ads_video"
   
class AdsType(str,Enum):
    quick_ads = "quick_ads"
    custom_ads = "custom_ads"
      
        
class Ads(Document):
    title:str
    description:Optional[str]
    image: Optional[List[Link[AdsImages]]] = None
    video: Optional[List[Link[AdsVideos]]] = None
    ads_type:AdsType = AdsType.quick_ads
    ads_status = AdsStatus.on_review
    budget:int
    owner_id: PydanticObjectId
    
    class Settings:
        name = "ads"
        
        
class AdsNotification(Document):
    name:str
    image:str
    title:str
    ads_type:str
    status:AdsStatus = AdsStatus.on_review
    ads_id:PydanticObjectId
    owner_id: PydanticObjectId
    
    class Settings:
        name = "ads_notifications"
  
        
class AdsSchema(BaseModel):
    title:str
    description:Optional[str]
    images: Optional[list]
    videos: Optional[list]
    ads_type:AdsType
    budget:int
    