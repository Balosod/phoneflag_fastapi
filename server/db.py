from beanie import init_beanie
import motor.motor_asyncio

from server.models.user import User
from server.models.device import Device,DeviceImage
from server.models.order import Order
from server.models.device_feedback import DeviceFeedback
from server.models.statistic import TotalStatistic
from server.models.notification import Notification
from server.models.tracking import Tracking
from server.models.insurance import Insurance,InsuranceDocument,InsuredUser
from server.models.ads import Ads,AdsImages,AdsVideos,AdsNotification


from .settings import CONFIG_SETTINGS

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(CONFIG_SETTINGS.DATABASE_URL)
    db_name = client[CONFIG_SETTINGS.DATABASE_NAME]

    await init_beanie(database=db_name, document_models=[User,Device,Order,DeviceImage,DeviceFeedback,
                                                         Notification,TotalStatistic,Tracking,
                                                         Insurance,InsuranceDocument,InsuredUser,
                                                         Ads,AdsImages,AdsVideos,AdsNotification])

