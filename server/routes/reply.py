from fastapi import APIRouter, Depends,status, Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from server.models.user import User
from beanie.operators import RegEx,And,Or,In
from server.models.device import Device
from server.models.order import Order
from server.models.device_feedback import DeviceFeedback,ReplySchema



router = APIRouter()


@router.post("/",status_code = 200)
async def reply(data:ReplySchema,response:Response, Authorize:AuthJWT = Depends()):
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await User.find_one(User.email == current_user)
    
    feedback_exist = await DeviceFeedback.get(data.review_id)
    if feedback_exist:
        feedback_exist.replys.append({"name":user.username,"reply":data.reply})
        await feedback_exist.save()
        return {"message":"Reply successfully sent"}
    else:
        response.status_code = 400
        return {"message":"Review does not exist"}
    
    