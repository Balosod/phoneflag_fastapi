from fastapi import APIRouter, Depends,status, Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from server.models.user import User
from beanie.operators import RegEx,And,Or,In
from server.models.device import Device
from server.models.order import Order
from server.models.device_feedback import DeviceFeedback,ReviewSchema



router = APIRouter()


@router.post("/",status_code = 200)
async def review(data:ReviewSchema,response:Response, Authorize:AuthJWT = Depends()):
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await User.find_one(User.email == current_user)
    
    order_exist = await Order.find_one(And((Order.owner_id == user.id),(Order.device_id == data.device_id)))
    if order_exist:
        feedback_exist = await DeviceFeedback.find_one(DeviceFeedback.device_id == data.device_id)
        if feedback_exist:
            feedback_exist.review = data.review
            await feedback_exist.save()
            return {"message":"feedback successfully created"}
        
        else:
            feedback = DeviceFeedback(
                name = user.username,
                review = data.review,
                owner_id = user.id,
                device_id = data.device_id
            )
            await feedback.create()
            return {"message":"feedback successfully created"}
    else:
        response.status_code = 400
        return {"message":"You have not Order this device"}