from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from beanie.operators import RegEx,And,Or,In,GTE,LTE, GT,LT
from ..utils.filter_helper import filters
from server.models.user import User
from server.models.device import Device



from typing import Optional, List
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.mongoengine import Filter


router = APIRouter()



@router.get("/brand/{brand}",status_code =200)
async def landing_page(brand:str) -> dict:
    
    devices = await Device.find(Device.brand == brand).to_list()

    return devices
    


@router.get("/filter",status_code =200)
async def filter(category:str|None=None,condition:str|None=None,color:str|None=None,
                brand:str|None=None,location:str|None=None,min_price:str|None=None,
                max_price:str|None=None) -> dict:
   
    devices = await filters(category,condition,color,brand,location,min_price,max_price)
   
    return devices
    