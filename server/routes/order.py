from fastapi import APIRouter, Depends,status, Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from server.models.user import User
from beanie.operators import RegEx,And,Or,In
from server.models.device import Device
from server.models.order import Order, OrderSechema
from server.models.statistic import TotalStatistic
from datetime import date



router = APIRouter()



@router.post("/",status_code = 200)
async def order(data:OrderSechema, Authorize: AuthJWT = Depends()) -> dict:
    
    today = date.today()
    
    Authorize.jwt_required()
    
    current_user = Authorize.get_jwt_subject()
    user = await User.find_one(User.email == current_user)
    
    context = {}
    device = await Device.find_one(Device.id==data.device_id)
    if device:
        order = Order(
            device_id = data.device_id,
            owner_id = user.id
        )
        await order.create()
        
        device.times_bought += 1
        await device.save()
        
       
        
        if device.owner_id == user.id:
            user.boughts += 1
            user.sales += 1
            await user.save()
        
        else:
            seller = await User.get(device.owner_id)
            seller.sales += 1
            await seller.save()
            
            user.boughts += 1
            await user.save()
        
        total_statistic_data = await TotalStatistic.find_one(TotalStatistic.date == today.strftime("%b-%d-%Y"))
        if total_statistic_data:
            updated_statistic_data = await TotalStatistic.get(total_statistic_data.id)
            updated_statistic_data.reach += device.discount_price
            await updated_statistic_data.save()
        else:
            new_statistic_data = TotalStatistic(date = today.strftime("%b-%d-%Y"),
                                           reach= device.discount_price)
            await new_statistic_data.create()
        return {"message":"Order successfully created"}
    else:
        response.status_code = 400
        return {"message":"Device not available"}