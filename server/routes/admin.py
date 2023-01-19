from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from beanie.operators import RegEx,And,Or,In
from server.models.property import Property
from server.models.booking_history import Booking
from server.models.statistic import Statistic
from server.models.user import User
from datetime import date





router = APIRouter()

today = date.today()

@router.get("/landing/page",status_code =200)
async def admin_landing_page() -> dict:
    
    #Authorize.jwt_required()
    
    data = []
    total_sales = 0
    check_in = 0
    check_out = 0
    statistic_list = []
    cities_list = {}
    booked_property = await Booking.find().to_list()
    for item in booked_property:
        property_obj = await Property.find_one(And((Property.id == item.property_id),(Property.property_type == "EVC_Apartment")))
        if property_obj:
            try:
                cities_list[property_obj.nearest_area] += 1 
            except:
                cities_list[property_obj.nearest_area] = 1 
            total_sales += item.apply_discount
            check_in += item.check_in_number
            if item.check_in == "monday1" and item.check_in_number == 0:
                check_in +=1
                new_check_in = await Booking.get(item.id)
                new_check_in.check_in_number = 1
                await new_check_in.save()
            check_out += item.check_out_number
            if item.check_out == "friday1" and item.check_out_number == 0:
                check_out +=1
                new_check_out = await Booking.get(item.id)
                new_check_out.check_out_number = 1
                await new_check_out.save()
                
    statistic = await Statistic.find().to_list()
    
    for item in statistic:
        property_obj = await Property.find_one(And((Property.id == item.property_id),(Property.property_type == "EVC_Apartment")))
        if property_obj:
            statistic_list.append(item)
    
    sorted_cities = sorted(cities_list.items(), key=lambda x:x[1],reverse=True)[0:3]
    top_cites = dict(sorted_cities)
    
    
    data.append(top_cites)    
    data.append({"total_sales":total_sales}) 
    data.append({"check_in":check_in}) 
    data.append({"check_out":check_out}) 
    data.extend(statistic_list)    
          
    return data

@router.get("/all/approved/property",status_code =200)
async def all_approved_property() -> dict:
    
    #Authorize.jwt_required()
    
    all_property = await Property.find(Property.status == "Approve", fetch_links=True).to_list()

    return all_property


@router.get("/all/property",status_code =200)
async def all_property() -> dict:
    
    #Authorize.jwt_required()
    
    all_property = await Property.find(fetch_links=True).to_list()

    return all_property


@router.get("/approve/property/{ID}",status_code =201)
async def approve_a_property(ID:PydanticObjectId,response:Response) -> dict:
    
    #Authorize.jwt_required()
    
    try:
        property_obj = await Property.find_one(Property.id == ID,fetch_links=True)
        property_obj.status = "Approve"
        await property_obj.save()

        return {"message":"Property has been Approved"}
    except:
        response.status_code = 400
        return {"message":"Something Went Wrong"}
    
    
@router.get("/reject/property/{ID}",status_code =201)
async def reject_a_property(ID:PydanticObjectId,response:Response) -> dict:
    
    #Authorize.jwt_required()
    
    try:
        property_obj = await Property.find_one(Property.id == ID,fetch_links=True)
        property_obj.status = "Reject"
        await property_obj.save()

        return {"message":"Property has been Rejected"}
    except:
        response.status_code = 400
        return {"message":"Something Went Wrong"}
    
    
@router.get("/all/affiliate",status_code =200)
async def get_all_affiliate() -> dict:
    
    #Authorize.jwt_required()
    all_affiliate = []
    affiliate_obj = await User.find(And((User.is_affiliate == True),(User.active == True)), fetch_links=True).to_list()
    
    all_affiliate.append({"total_affiliate":len(affiliate_obj)})
    all_affiliate.extend(affiliate_obj)
    return all_affiliate

@router.get("/all/user",status_code =200)
async def get_all_user() -> dict:
    
    #Authorize.jwt_required()
    all_user = []
    user_obj = await User.find(And((User.is_affiliate == False),(User.active == True)), fetch_links=True).to_list()
    
    all_user.append({"total_user":len(user_obj)})
    all_user.extend(user_obj)
    return all_user


@router.get("/add/affiliate/{email}",status_code =201)
async def add_an_affiliate(email:str,response:Response) -> dict:
    
    #Authorize.jwt_required()
    
    try:
        user = await User.find_one(User.email == email)
        user.is_affiliate = True
        user.created = today.strftime("%B %d, %Y")
        await user.save()

        return {"message":"User Successfully added as an affiliate"}
    except:
        response.status_code = 400
        return {"message":"Something Went Wrong"}