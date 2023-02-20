
import base64
import uuid
from ..utils.s3_storage import client
from ..settings import CONFIG_SETTINGS



async def upload_document_to_file_path(documents,model_name):
    document_obj_list = []
    for document in documents:
        document_name = str(uuid.uuid4())[:10] + '.pdf'
        document_as_bytes = str.encode(document) 
        document_recovered = base64.b64decode(document_as_bytes)
        
        with open("server/media/document/uploaded_" + document_name, "wb") as f:
            f.write(document_recovered)
            
        upload_document = model_name(document=f"http://localhost:8000/media/document/uploaded_{document_name}")
        document_obj_list.append(upload_document)
        await upload_document.create()
    return document_obj_list
    
async def upload_document_to_S3_bucket(documents,model_name):
    document_obj_list = []
    for document in documents:
        document_name = str(uuid.uuid4())[:10] + '.pdf'
        document_as_bytes = str.encode(document) 
        document_recovered = base64.b64decode(document_as_bytes)
        
        client.put_object(
        Bucket=CONFIG_SETTINGS.BUCKET,
        Body=document_recovered,
        Key=f"image/{document_name}",
        ACL=CONFIG_SETTINGS.ACL,
        ContentType="image/png"
        )
            
        upload_document = model_name(document=f"https://postatusapistorage.nyc3.digitaloceanspaces.com/document/{document_name}")
        document_obj_list.append(upload_document)
        await upload_document.create()
    return document_obj_list