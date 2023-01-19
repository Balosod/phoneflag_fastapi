from typing import Optional,List
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel



    
    
class Statistic(Document):
    date:str
    reach:int
    property_id: PydanticObjectId
    
    
    class Settings():
        name = "statistics"