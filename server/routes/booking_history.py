from fastapi import APIRouter, Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from server.models.booking_history import Booking,BookingSchema
from server.models.statistic import Statistic
from server.models.user import User
from server.models.property import Property
from datetime import date



router = APIRouter()

today = date.today()


async def get_ID(itemID):
    propertyID = await Property.get(itemID, fetch_links=True)
    if propertyID:
        return propertyID.id
    else:
        return None
    

@router.post("/create/{itemID}", status_code = 200)
async def book_a_property(data:BookingSchema,itemID:PydanticObjectId,response:Response, Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    Id = await get_ID(itemID)

    if Id:
        booking = Booking(
            check_in=data.check_in,
            check_out=data.check_out,
            apply_discount=data.apply_discount,
            owner_id=user.id,
            property_id=Id
            )
        
        await booking.create()
        
        statistic_data = await Statistic.find_one(Statistic.date == today.strftime("%b-%d-%Y") )
        if statistic_data:
            updated_statistic_data = await Statistic.get(statistic_data.id)
            updated_statistic_data.reach += data.apply_discount
            await updated_statistic_data.save()
        else:
            new_statistic_data = Statistic(date = today.strftime("%b-%d-%Y"),
                                           reach= data.apply_discount,
                                           property_id=Id
                                           )
            await new_statistic_data.create()
            
        return {"message":"Booking successfully added"}
    else:
        response.status_code = 400
        return HTTPException(
            status_code=400,
            detail="Property doesn't exit any more"
        )
    


@router.get("/get/all",status_code =200)
async def get_your_booked_property(Authorize: AuthJWT = Depends()) -> dict:
    
    Authorize.jwt_required()
    
    current_user = Authorize.get_jwt_subject()
    user = await User.find_one(User.email == current_user)
    
    bookings = []
    user_booked_property = await Booking.find(Booking.owner_id == user.id).to_list()
    for item in user_booked_property:
        Id = item.property_id
        property_obj = await Property.get(Id, fetch_links=True)
        bookings.append(property_obj)
         
    return bookings 
