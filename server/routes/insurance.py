from fastapi import APIRouter, Depends,status, Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from server.models.user import User
from beanie.operators import RegEx,And,Or,In
from ..utils import upload_document_helper
from ..settings import CONFIG_SETTINGS
from server.models.insurance import Insurance,InsuranceDocument, InsuredUser,InsuranceSchema




router = APIRouter()


@router.post("/add/document",status_code = 200)
async def insured_device(data:InsuranceSchema, response:Response, Authorize:AuthJWT = Depends()):
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    
    if CONFIG_SETTINGS.USE_SPACES:
        document_obj = await upload_document_helper.upload_document_to_S3_bucket(data.insurance_documents,InsuranceDocument)
    else:
        document_obj = await upload_document_helper.upload_document_to_file_path(data.insurance_documents,InsuranceDocument)
        
    
    insured_device = Insurance(
        fullname=data.fullname,
        email=data.email,
        phone_number=data.phone_number,
        employment_status=data.employment_status,
        contact_address=data.contact_address,
        profession=data.profession,
        device_brand=data.device_brand,
        device_model=data.device_model,
        purchase_price=data.purchase_price,
        insurance_company=data.insurance_company,
        insurance_policy=data.insurance_policy,
        insurance_documents=document_obj,
        owner_id=user.id
    )
    await insured_device.create()
    
    insured_user = await InsuredUser.find_one(InsuredUser.owner_id == user.id)
    if insured_user:
        pass
    else:
        new_insured_user = InsuredUser(
            owner_id = user.id
        )
        await new_insured_user.create()
    return {"message":"insurance document submitted"}


@router.post("/update/document/{ID}",status_code = 200)
async def update_insured_device(ID:PydanticObjectId,data:InsuranceSchema, response:Response, Authorize:AuthJWT = Depends()):
    
    Authorize.jwt_required()
    
    if CONFIG_SETTINGS.USE_SPACES:
        if (data.insurance_documents and data.insurance_documents != ""):
            document_obj = await upload_document_helper.upload_document_to_S3_bucket(data.insurance_documents,InsuranceDocument)
    else:
        if (data.insurance_documents and data.insurance_documents != ""):
            document_obj = await upload_document_helper.upload_document_to_file_path(data.insurance_documents,InsuranceDocument)
    
    insured_device = await Insurance.get(ID)
    if insured_device:
        if (data.fullname and data.fullname != ""):
            insured_device.fullname = data.fullname
        if (data.email and data.email != ""):
            insured_device.email = data.email
        if (data.phone_number and data.phone_number != ""):
            insured_device.phone_number = data.phone_number
        if (data.employment_status and data.employment_status != ""):
            insured_device.employment_status = data.employment_status
        if (data.contact_address and data.contact_address != ""):
            insured_device.contact_address = data.contact_address
        if (data.profession and data.profession != ""):
            insured_device.profession = data.profession
        if (data.device_brand and data.device_brand != ""):
            insured_device.device_brand = data.device_brand
        if (data.device_model and data.device_model != ""):
            insured_device.device_model = data.device_model
        if (data.purchase_price and data.purchase_price != ""):
            insured_device.purchase_price = data.purchase_price
        if (data.insurance_company and data.insurance_company != ""):
            insured_device.insurance_company = data.insurance_company
        if (data.insurance_policy and data.insurance_policy != ""):
            insured_device.insurance_policy = data.insurance_policy
        if (data.insurance_documents and data.insurance_documents != ""):
            insured_device.insurance_documents = document_obj  
        await insured_device.save()
        
        return {"message":"Data successfully updated"}
    else:
        response.status_code = 400
        return{"message":"data not found or Deleted "}
    
    
@router.get("/delete/document/{ID}",status_code = 200)
async def delete_insured_device(ID:PydanticObjectId,response:Response, Authorize:AuthJWT = Depends()):
    
    Authorize.jwt_required()
    try:
        insured_device = await Insurance.get(ID)
        await insured_device.delete()
        return {"message":"Insurance document deleted"}
    except:
        return {"message":"Document deleted or does not exist"}