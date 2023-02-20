from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from beanie.operators import RegEx,And,Or,In
from ..utils import upload_image_helper, upload_video_helper
from ..settings import CONFIG_SETTINGS
from server.models.user import User
from server.models.ads import Ads,AdsImages,AdsVideos, AdsSchema,AdsNotification


router = APIRouter()

@router.post("/publish",status_code=201)
async def publish_ads(data:AdsSchema,response:Response,Authorize: AuthJWT = Depends()) -> dict:
    
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    
    
    if CONFIG_SETTINGS.USE_SPACES:
        image_obj = await upload_image_helper.upload_image_to_S3_bucket(data.images,AdsImages)
        video_obj = await upload_video_helper.upload_video_to_S3_bucket(data.videos,AdsVideos)
    else:
        image_obj = await upload_image_helper.upload_image_to_file_path(data.images,AdsImages)
        video_obj = await upload_video_helper.upload_video_to_file_path(data.videos,AdsVideos)
        
    ads_obj = Ads(
        title = data.title,
        description = data.description,
        image = image_obj,
        video = video_obj,
        ads_type = data.ads_type,
        budget = data.budget,
        owner_id = user.id
    )
    
    await ads_obj.create()
 
    notification_obj = AdsNotification(
        name = user.username,
        image = user.img,
        title = data.title,
        ads_type = data.ads_type,
        ads_id = ads_obj.id,
        owner_id = user.id    
    )
    await notification_obj.create()
    
    return {"message":"ads successfully published"}