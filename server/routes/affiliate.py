from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from beanie.operators import RegEx,And,Or,In
from server.models.property import Property
from server.models.user import User




router = APIRouter()


@router.get("/all/property",status_code =200)
async def all_property(respone:Response, Authorize: AuthJWT = Depends()) -> dict:
    
    Authorize.jwt_required()
    
    current_user = Authorize.get_jwt_subject()
    user = await User.find_one(User.email == current_user)
    
    if user.is_affiliate:
        all_property = await Property.find(Property.owner_id == user.id, fetch_links=True).to_list()
        return all_property
    else:
        response.status_code = 401
        return {"message":"not an affiliate"}
