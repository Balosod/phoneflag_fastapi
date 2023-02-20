from typing import Optional, List
from beanie import Document,PydanticObjectId, Link
from pydantic import BaseModel, EmailStr, Field,validator
from enum import Enum
from datetime import date

today = date.today()

class InsuranceCompany(str,Enum):
    axa_mansard_insurance_plc = "axa_mansard_insurance_plc"
    leadway_assurance = "leadway_assurance"
    heirs_insurance_limited = "heirs_insurance_limited"
    
class InsuranceStatus(str,Enum):
    pending = "pending"
    payment_done = "payment_done"
    
class InsuranceDocument(Document):
    document:str
    
    class Settings:
        name = "insurance_document"
        
class Insurance(Document):
    insurance_id:Optional[str]
    fullname:str
    email:EmailStr
    phone_number:str
    employment_status:str
    contact_address:str
    profession:str
    device_brand:str
    device_model:str
    purchase_price:str
    insurance_company:InsuranceCompany
    insurance_policy:str
    date_of_request:str = today.strftime("%d %b %Y")
    status:InsuranceStatus = InsuranceStatus.pending
    insurance_documents:Optional[List[Link[InsuranceDocument]]] = None
    owner_id: PydanticObjectId
    
    
    class Settings:
        name = "insurances"
        
        
class InsuredUser(Document):
    owner_id:PydanticObjectId
    
    class Settings:
        name = "insured_user"
    
    
class InsuranceSchema(BaseModel):
    fullname:str
    email:EmailStr
    phone_number:str
    employment_status:str
    contact_address:str
    profession:str
    device_brand:str
    device_model:str
    purchase_price:str
    insurance_company:InsuranceCompany
    insurance_policy:str
    insurance_documents:Optional[list] = None
    