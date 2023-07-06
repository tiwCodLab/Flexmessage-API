from fastapi import APIRouter,HTTPException,Body, UploadFile,File,Form
from models.flexaver_models import Flexmessage ,CodeDict
from schemas.flexaver_schema import  datas_serializer
from config.db import collection
from config.firebase_config import config
import pyrebase

user = APIRouter()

current_id = 0
@user.post("/api/")
async def create_flexmessage(data:Flexmessage):
    global current_id
    try:
        # Create the data to be inserted
        current_id += 1
        data.id = current_id
        # Insert data into the database
        inserted_id = collection.insert_one(data.dict()).inserted_id
        return {"status": "Success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# upload img
@user.post("/upload/image/")
async def upload_file(file: UploadFile = File(...)):
    try:
        latest_document = collection.find().sort('id', -1).limit(1).next()
        current_counter = latest_document['id']
        # Increment the counter
        new_counter = current_counter + 1
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()

        file.filename = f"{new_counter}.jpg"
        contents = await file.read()
    
        storage.child(file.filename).put(contents)
        file_url = storage.child(file.filename).get_url(None)
        print(file_url)
    # Insert data into the database
        return {"status": "Success","urlimg":file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# เพิ่มข้อมูล
@user.post("/api/flexmessage/")
async def create_flex_message(data: Flexmessage ):
    try:
        # เรียกดูในฐานข้อมูลว่าถึง id ไหน
        latest_document = collection.find().sort('id', -1).limit(1).next()
        current_counter = latest_document['id']
        # Increment the counter
        new_counter = current_counter + 1
        # Update the counter value in the database

        imgName = f"{new_counter}.jpg"
        # ฐานข้อมูล firebase
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()

        file_url = storage.child(imgName).get_url(None)
        print(file_url)

        data.id = new_counter
        data.image = str(file_url)
        # Insert data into the database
        inserted_id = collection.insert_one(data.dict()).inserted_id
        return {"status": "Success"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# เรียกดูข้อมูลทั้งหมด
@user.get("/api/flexmessage/")
async def get_all_flex_messages(page: int = 1, per_page: int = 10):
    try:
        # Calculate the starting index
        start_index = (page - 1) * per_page
        # Query the database to get a slice of data
        flex_messages = collection.find().skip(start_index).limit(per_page)
        # Serialize the data
        serialized_data = datas_serializer(flex_messages)
        return {"message": serialized_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user.get("/api/flexmessage/{message_id}")
async def get_flex_message(message_id: int):
    try:
        flex_message = collection.find_one({"id": message_id})
        if flex_message:
            serialized_data = datas_serializer([flex_message])
            return { "message": serialized_data}
        else:
            raise HTTPException(status_code=404, detail="Flex message not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user.put("/api/flexmessage/{message_id}")
async def update_flex_message(message_id: int, name: str = Body(...), category: str = Body(...), code_flexmessage: CodeDict = Body(...), status: bool = Body(False)):
    try:
        # Find the flex message by ID
        flex_message = collection.find_one({"id": message_id})
        if flex_message:
            # Update the flex message fields
            flex_message["name"] = name
            flex_message["category"] = category
            flex_message["code_flexmessage"] = code_flexmessage.dict()
            flex_message["status"] = status

            # Update the flex message in the database
            collection.update_one({"id": message_id}, {"$set": flex_message})
            return {"status": "Success"}
        else:
            raise HTTPException(status_code=404, detail="Flex message not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@user.delete("/api/flexmessage/{message_id}")
async def delete_flex_message(message_id: int):
    try:
        result = collection.delete_one({"id": message_id})
        if result.deleted_count > 0:
            return {"status": "Ok", "message": "Flex message deleted"}
        else:
            raise HTTPException(status_code=404, detail="Flex message not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user.get("/api/flexmessage/category/{category}")
async def get_flex_messages_by_category(category: str):
    try:
        # Query the database to get flex messages with the specified category
        flex_messages = collection.find({"category": category})
        
        serialized_data = datas_serializer(flex_messages)
        
        return {"message": serialized_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


