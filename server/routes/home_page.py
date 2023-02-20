from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from beanie.operators import RegEx,And,Or,In
from server.models.user import User
from server.models.device import Device


router = APIRouter()



@router.get("/page",status_code =200)
async def landing_page() -> dict:
    
    sponsored = []
    todays_deal = []
    best_sellers = []
    devices = await Device.find().to_list()
    for device in devices:
        if device.sponsored == True:
            sponsored.append(device)
        if device.todays_deal == True:
            todays_deal.append(device)
        if device.best_sellers == True:
            best_sellers.append(device)
    
    return {"sponsored":sponsored,"todays_deal":todays_deal,"best_sellers":best_sellers}

