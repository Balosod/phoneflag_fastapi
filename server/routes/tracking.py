from fastapi import APIRouter, Depends,status, Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from server.models.user import User
from beanie.operators import RegEx,And,Or,In
from server.models.tracking import Tracking, TrackingSchema




router = APIRouter()


@router.post("/device",status_code = 200)
async def track_device(data:TrackingSchema, response:Response, Authorize:AuthJWT = Depends()):
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    
    track_device = Tracking(
        device_model=data.device_model,
        imel_number=data.imel_number,
        device_condition=data.device_condition,
        last_backup=data.last_backup,
        email=data.email,
        owner_id=user.id
    )
    await track_device.create()
    
    return {"message":"tracking requested"}