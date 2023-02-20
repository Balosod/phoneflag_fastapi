from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from beanie.operators import RegEx,And,Or,In
from ..utils import upload_image_helper
from ..settings import CONFIG_SETTINGS
from server.models.user import User
from server.models.device import Device,DeviceImage,DeviceSchema
from server.models.notification import Notification
from datetime import datetime


router = APIRouter()



@router.post("/publish",status_code=201)
async def publish_device(data:DeviceSchema,response:Response,Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    try:
        if CONFIG_SETTINGS.USE_SPACES:
            image_obj = await upload_image_helper.upload_image_to_S3_bucket(data.images,DeviceImage)
        else:
            image_obj = await upload_image_helper.upload_image_to_file_path(data.images,DeviceImage)
        
        # price_list = []
        device = Device(
            name = data.name,
            category = data.category,
            brand = data.brand,
            first_condition = data.first_condition,
            second_condition = data.second_condition,
            internal_storage = data.internal_storage,
            screen_size = data.screen_size,
            battery_capacity = data.battery_capacity,
            operating_system = data.operating_system,
            weight = data.weight,
            color = data.color,
            description = data.description,
            minimum_order = data.minimum_order,
            discount_price = data.discount_price,
            location = data.location,
            off_price = data.off_price,
            images=image_obj,
            owner_id=user.id
        )
            
        await device.create()
        now = datetime.now()
        print(now.strftime("%I:%M:%S"))
        
        notification = Notification(
            time=now.strftime("%I:%M:%S"),
            action=f"New product Added <<{data.name}>>"
        )
        await notification.create()
        
        return {"message":"device Successfully published"}
    except:
        response.status_code = 400
        return {"message":"Something went wrong"}