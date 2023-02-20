from fastapi import APIRouter, Depends,status, Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from server.models.user import User
from beanie.operators import RegEx,And,Or,In
from server.models.device import Device
from server.models.device_feedback import DeviceFeedback
from server.models.order import Order


router = APIRouter()




@router.get("/{ID}",status_code = 200)
async def detail(ID:PydanticObjectId, response:Response, Authorize: AuthJWT = Depends()) -> dict:
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await User.find_one(User.email == current_user)
    
    total_ratings = 0
    ratings_average = 0
    total_product_sold = 0
    divisor = 0
    modify_ratings = {"5":0,"4":0,"3":0,"2":0,"1":0}
    
    context = {"device_detail":"","user":"","reviews":"","ratings":"","total_reviews":"","total_ratings":"","ratings_average":"","total_product_sold":""}
    
    device = await Device.find_one(Device.id==ID, fetch_links=True)
    if device:
        reviews = await DeviceFeedback.find(DeviceFeedback.device_id == device.id).to_list()
        for rate in reviews:
            divisor +=1
            if rate.rating == "5":
                modify_ratings["5"] = modify_ratings["5"]+1
                total_ratings+=5
            elif rate.rating == "4":
                modify_ratings["4"] = modify_ratings["4"]+1
                total_ratings+=4
            elif rate.rating == "3":
                modify_ratings["3"] = modify_ratings["3"]+1
                total_ratings+=3
            elif rate.rating == "2":
                modify_ratings["2"] = modify_ratings["2"]+1
                total_ratings+=2
            elif rate.rating == "1":
                modify_ratings["1"] = modify_ratings["1"]+1
                total_ratings+=1
        ratings_average += round((total_ratings/divisor),1)
        
        order = await Order.find(Order.device_id==device.id).to_list()
        
        context["user"] = user
        context["device_detail"] = device
        context["reviews"] = reviews
        context["total_reviews"] = len(reviews)
        context["ratings_average"] = ratings_average
        context["total_ratings"] = total_ratings
        context["ratings"] = modify_ratings
        context["total_product_sold"] = len(order)
        
        return context
    else:
        return {"message":"Device does not exist"}