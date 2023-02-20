from typing import Optional
from beanie import Document



class Notification(Document):
    time:str
    action:str
    
    class Settings:
        name ="notifications"