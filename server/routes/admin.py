from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from beanie.operators import RegEx,And,Or,In
from server.models.user import User
from server.models.device import Device
from server.models.order import Order
from server.models.statistic import TotalStatistic
from server.models.notification import Notification
from server.models.tracking import Tracking
from server.models.insurance import Insurance, InsuredUser,InsuranceCompany
from server.models.ads import Ads, AdsNotification
from datetime import date



router = APIRouter()




@router.get("/dashboard",status_code =200)
async def dashboard() -> dict:
    context = {}
    
    users_id = []
    sellers = []
    buyers = []
    buyers_id = []
    orders = await Order.find().to_list()
    users = await User.find().to_list()
    for order in orders:
        users_id.append(order.device_id)
        buyers_id.append(order.owner_id)
        
    for Id in list(set(users_id)):
        device = await Device.get(Id)
        user = await User.get(device.owner_id)
        sellers.append(user.dict())
    
    for Id in list(set(buyers_id)):
        user = await User.get(Id)
        buyers.append(user.dict())
    
    monthly_sales = await TotalStatistic.find().to_list()
    total_devices_tracked = await Tracking.find(Tracking.status == "tracking").to_list()
    total_devices_insured = await Insurance.find(Insurance.status == "payment_done").to_list()
    top_sellers = sorted(sellers, key=lambda x:x['sales'],reverse=True)
    top_buyers = sorted(buyers, key=lambda x:x['boughts'],reverse=True)
    
    context["total_order"] = len(orders)
    context["total_registered_user"] = len(users)
    context["total_devices_insured"] = len(total_devices_insured)
    context["total_devices_tracked"] = len(total_devices_tracked)
    context["monthly_sales"] = monthly_sales
    context["top_buyers"] = top_buyers
    context["top_sellers"] = top_sellers
    
    
    return context


@router.get("/marketplace",status_code =200)
async def marketplace() -> dict:
    
    today = date.today()
    
    context = {}
    
    top_devices =[]
    total_sales = 0
    sales_this_month = 0
    profitable_categories = {}
    
    devices = await Device.find().to_list()
    for device in devices:
        top_devices.append(device.dict())
    best_selling_product = sorted(top_devices, key=lambda x:x['times_bought'],reverse=True)[0:1]
    top_selling_product = sorted(top_devices, key=lambda x:x['times_bought'],reverse=True)[0:5]
    
    sales = await TotalStatistic.find().to_list()
    for sale in sales:
        total_sales += sale.reach
        
    orders  = await Order.find().to_list()
    
    todays_date = today.strftime("%b-%d-%Y")
    splited_date = todays_date.split("-")
    month = splited_date[0]
    year = splited_date[2]
    
    date_pattern = rf'\b{month}\S+{year}\b'
    monthly_sales = await TotalStatistic.find(RegEx(TotalStatistic.todays_date,date_pattern,"i" )).to_list()
    
    for sales in monthly_sales:
        sales_this_month += sales.reach
  
    
    
    bought_devices = await Device.find(Device.times_bought > 0).to_list()
    for bought_device in bought_devices:
        try:
            profitable_categories[bought_device.category.value] += bought_device.discount_price
        except:
            profitable_categories[bought_device.category.value] = bought_device.discount_price
    
    categories_sorted_by_price = sorted(profitable_categories.items(), key=lambda x:x[1],reverse=True)
     
    notification = await Notification.find().to_list()
        
    context["best_selling_product"] = best_selling_product
    context["top_selling_product"] = top_selling_product
    context["total_sales"] = total_sales
    context["total_orders"] = len(orders)
    context["items_on_sales"] = len(devices)
    context["sales_this_month"] = sales_this_month
    context["profitable_categories"] = dict(categories_sorted_by_price)
    context["notification"] = notification
    
    return context




@router.get("/insurance",status_code =200)
async def insurance() -> dict:
    
    context = {}
    
    insurance_companies = len(list(InsuranceCompany))
    total_insured_user  = await InsuredUser.find().to_list()
    total_register_device = await Insurance.find(fetch_links=True).to_list()
    total_insured_devices = await Insurance.find(Insurance.status == "payment_done", fetch_links=True).to_list()
    
    context["total_insured_user"] =len(total_insured_user)
    context["total_insured_devices"] = len(total_insured_devices)
    context["insurance_companies"] = insurance_companies
    context["total_register_device"] = len(total_register_device)
    context["data"] = total_register_device
    return context




@router.get("/tracking",status_code =200)
async def tracking() -> dict:
    
    context = {}
  
    
    total_register_device = await Tracking.find().to_list()
    total_tracked_devices = await Tracking.find(Tracking.status == "tracking").to_list()
    
    context["total_tracked_devices"] = len(total_tracked_devices)
    context["total_register_device"] = len(total_register_device)
    context["data"] = total_register_device
    
    return context


@router.get("/ads",status_code =200)
async def ads() -> dict:
    
    context = {}
  
    users = await User.find().to_list()
    ads =  await Ads.find().to_list()
    recent_campaign = await AdsNotification.find().to_list()
    
    context["total_campaign"] = len(ads)
    context["total_audience"] = len(users)
    context["recent_campaign"] = recent_campaign
    
    
    return context




@router.get("/account",status_code =200)
async def account() -> dict:
    
    users = await User.find().to_list()
    
    return users
    