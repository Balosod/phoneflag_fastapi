from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends,Response
from passlib.context import CryptContext
from typing import List
import re
from ..utils import auth_service
from ..utils.helpers import fm
from ..utils.helpers import EmailManager
from starlette.responses import JSONResponse

# from auth.auth_handler import signJWT
from fastapi_jwt_auth import AuthJWT


from server.models.user import (
    User,
    UserLogin,
    OtpSchema,
    EmailSchema,
    SuccessResponseModel,
    ErrorResponseModel
)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


@router.post("/signup", response_description="User added to the database",status_code=201)
async def create_account(user: User,response:Response) -> dict:
    
    email_regex = r'com$'
    match = re.search(email_regex, user.email)
    if not match:
        response.status_code = 400
        return HTTPException(
            status_code=400,
            detail="Email is invalid"
        )
        
    user_exists = await User.find_one(User.email == user.email)

    if user_exists:
        response.status_code = 400
        return HTTPException(
            status_code=400,
            detail="Email already exists!"
        )

    user.password = pwd_context.hash(user.password)
    await user.create() 
    message  = EmailManager.send_welcome_msg(user.email)
    await fm.send_message(message)
    return SuccessResponseModel(user, 201, "Account successfully created!" )

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