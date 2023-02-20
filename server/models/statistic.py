from typing import Optional,List
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel
from enum import Enum


    

class TotalStatistic(Document):
    todays_date:str
    reach:int

    
    
    class Settings():
        name = "total_statistics"
        