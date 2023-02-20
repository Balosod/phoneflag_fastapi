from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends,Response
from passlib.context import CryptContext
from typing import List
import re
import base64
import uuid
from ..utils import auth_service
from ..utils.helpers import api_instance
from ..utils.helpers import EmailManager
from ..utils.s3_storage import client
from ..settings import CONFIG_SETTINGS
from starlette.responses import JSONResponse


from fastapi_jwt_auth import AuthJWT


from server.models.user import (
    User,
    RegistrationSchema,
    UserLogin,
    PasswordSchema,
    OtpSchema,
    ImageSchema,
    ProfileDataSchema,
    EmailSchema,
    SuccessResponseModel,
    ErrorResponseModel
)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


@router.post("/signup", response_description="User added to the database",status_code=201)
async def create_account(data: RegistrationSchema,response:Response) -> dict:
    
    email_regex = r'com$'
    match = re.search(email_regex, data.email)
    if not match:
        response.status_code = 400
        return HTTPException(
            status_code=400,
            detail="Email is invalid"
        )
        
    user_exists = await User.find_one(User.email == data.email)

    if user_exists:
        response.status_code = 400
        return HTTPException(
            status_code=400,
            detail="Email already exists!"
        )

    hash_password = pwd_context.hash(data.password)
    
    user = User(
        name= data.username,
        email =data.email,
        password = hash_password
    )
    try:
        send_smtp_email  = EmailManager.send_welcome_msg(data.email)
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
        await user.create()
        return SuccessResponseModel(user, 201, "Account successfully created!" )
    
    except:
        return HTTPException(
            status_code=400,
            detail="User not created"
        )

@router.post("/auth/login", response_description="User login",status_code = 200)
async def login_user(user: UserLogin, response:Response, Authorize: AuthJWT = Depends()):
    user_acct = await User.find_one(User.email == user.email)

    if user_acct and user_acct.active and pwd_context.verify(user.password, user_acct.password):
        access_token = Authorize.create_access_token(subject=user.email)
        refresh_token = Authorize.create_refresh_token(subject=user.email)
        return {"access_token": access_token, "refresh_token": refresh_token}

    response.status_code = 400
    return HTTPException(
            status_code=400,
            detail="User with that email doesn't exist or password incorrect"
        )


@router.post("/refresh", response_description="Get new access token")
def get_new_access_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.post("/auth/verify", response_description="verify otp", status_code = 200)
async def verify_otp(data: OtpSchema):
    
    obj = await auth_service.verify_OTP(data.email,data.otp)
    return {"message":obj}


@router.post("/auth/resend", response_description="resend otp",status_code = 200)
async def resend_otp(data:EmailSchema):

    obj = await auth_service.resend_OTP(data.email)
    return {"message":obj}



# @router.get("/profile",status_code = 200)
# async def get_user_profile_data(response:Response, Authorize: AuthJWT = Depends()):
    
#     Authorize.jwt_required()
#     current_user = Authorize.get_jwt_subject()
    
#     user = await User.find_one(User.email == current_user)
#     if user:
#         return user
#     else:
#         response.status_code = 400
#         return{"message":"User not found"}



@router.post("/profile/image/update", status_code = 200, response_description="Upload profile image")
async def upload_profile_image(data:ImageSchema, response:Response, Authorize: AuthJWT = Depends()):
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    if user:
        if CONFIG_SETTINGS.USE_SPACES:
            img_name = str(uuid.uuid4())[:10] + '.png'
            image_as_bytes = str.encode(data.image) 
            img_recovered = base64.b64decode(image_as_bytes)
            
            client.put_object(
            Bucket=CONFIG_SETTINGS.BUCKET,
            Body=img_recovered,
            Key=f"image/{img_name}",
            ACL=CONFIG_SETTINGS.ACL,
            ContentType="image/png"
            )
                
            img_url = f"https://postatusapistorage.nyc3.digitaloceanspaces.com/image/{img_name}"
            
            user.img = img_url
            await user.save()
            
            return{"message":"image successfully uploaded."}
        else:
            img_name = str(uuid.uuid4())[:10] + '.png'
            image_as_bytes = str.encode(data.image) 
            img_recovered = base64.b64decode(image_as_bytes)
            
            with open("server/media/image/uploaded_" + img_name, "wb") as f:
                f.write(img_recovered)
                
            img_url = f"http://localhost:8000/media/image/uploaded_{img_name}"
            
            user.img = img_url
            await user.save()
            
            return{"message":"image successfully uploaded"}
    else:
        response.status_code = 400
        return{"message":"User not found"}
    

@router.post("/profile/update", status_code = 200, response_description="data updated")
async def update_profile_data(data:ProfileDataSchema, response:Response, Authorize: AuthJWT = Depends()):
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    if user:
        if (data.username and data.username != ""):
            user.username = data.username
        if (data.full_name and data.full_name != ""):
            user.full_name = data.full_name
        if (data.email and data.email != ""):
            email_regex = r'com$'
            match = re.search(email_regex, data.email)
            if not match:
                response.status_code = 400
                return HTTPException(
                    status_code=400,
                    detail="Email is invalid"
                )
            user.email = data.email
        if (data.store_name and data.store_name != ""):
            user.store_name = data.store_name
        if (data.phone and data.phone != ""):
            user.phone = data.phone
        if (data.address and data.address != ""):
            user.address = data.address
        await user.save()
        return {"message":"Data successfully updated"}
    else:
        response.status_code = 400
        return{"message":"User not found"}
    
    
    

@router.post("/profile/reset/password", status_code = 200, response_description="data updated")
async def reset_user_password(data:PasswordSchema, response:Response, Authorize: AuthJWT = Depends()):
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    if user:
        if pwd_context.verify(data.current_password, user.password):
            hash_password = pwd_context.hash(data.new_password)
            user.password = hash_password
            await user.save()
            return {"message":"Password successfully updated"}
        else:
            response.status_code = 400
            return {"message":"Current Password does not match"}
    else:
        response.status_code = 400
        return{"message":"User not found"}
    