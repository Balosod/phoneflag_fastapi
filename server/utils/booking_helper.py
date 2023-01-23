from beanie import init_beanie
import motor.motor_asyncio


from server.models.user import User
from server.models.property import Property,ApplicableDiscount,PropertyImages,PropertyVideos
from server.models.booking_history import Booking
from server.models.statistic import Statistic
from server.models.transaction import Transaction


from ..settings import CONFIG_SETTINGS

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(CONFIG_SETTINGS.DATABASE_URL)
    db_name = client[CONFIG_SETTINGS.DATABASE_NAME]

    await init_beanie(database=db_name, document_models=[User,Property,ApplicableDiscount,
                                                          PropertyImages,Booking,Statistic,
                                                          PropertyVideos,Transaction])
async def start_db():
    await init_db()

# async def check_booking():
#     booked_property = await Booking.find().to_list()
#     for item in booked_property:
#         if item.check_in_date == "monday1":
#                 new_check_in = await Booking.get(item.id)
#                 new_check_in.check_in_number = 1
#                 await new_check_in.save()    
#         if item.check_out_date == "friday1":
#             new_check_out = await Booking.get(item.id)
#             new_check_out.check_out_number = 1
#             await new_check_out.save()
#     return ("good one")


def check_booking():
    
    booked_property = Booking.find().to_list()
    for item in booked_property:
        if item.check_in_date == "monday1":
                new_check_in =  Booking.get(item.id)
                new_check_in.check_in_number = 1
                new_check_in.save()    
        if item.check_out_date == "friday1":
            new_check_out = Booking.get(item.id)
            new_check_out.check_out_number = 1
            new_check_out.save()
    return ("good one")




# def check_booking():
    
#     return "good one"
