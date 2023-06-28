from fastapi import APIRouter,HTTPException,Body
from models.flexaver_models import Flexmessage ,code_dict
from schemas.flexaver_schema import flexmessages_serializer, datas_serializer
from config.db import collection
user = APIRouter()

# กำหนด URI ของ MongoDB Atlas

@user.post("/api/flexmessage/")
async def create_upload_file(name: str = Body(...) ,category: str =  Body(...)  , code_flexmessage: code_dict =  Body(...)  , status: bool =  Body(False)):
    try:
        # Create the data to be inserted
        flex_message = Flexmessage(
            name=name,
            category=category,
            code_flexmessage=code_flexmessage.dict(),
            status=status
        )
        # Insert data into the database
        collection.insert_one(flex_message.dict()).inserted_id
        return {"status": "Success"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# async def create_upload_file(name: str ,category: str  , code: code_dict  , status: bool = False):
#     try:
#         # Create the data to be inserted
#         flex_message = Flexmessage(
#             name=name,
#             category=category,
#             code=code.dict(),
#             status=status
#         )
#         # Insert data into the database
#         collection.insert_one(flex_message.dict()).inserted_id
#         return {"status": "Success"}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@user.get("/api/flexmessage/")
async def get_all_flex_messages(page: int = 1, per_page: int = 10):
    try:
        # Calculate the starting index
        start_index = (page - 1) * per_page
        # Query the database to get a slice of data
        flex_messages = collection.find().skip(start_index).limit(per_page)
        # Serialize the data
        serialized_data = datas_serializer(flex_messages)
        return {"status": "Ok", "message": serialized_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user.get("/api/flexmessage/{message_id}")
async def get_flex_message(message_id: str):
    try:
        flex_message = collection.find_one({"id": message_id})
        if flex_message:
            serialized_data = datas_serializer([flex_message])
            return {"status": "Ok", "message": serialized_data}
        else:
            raise HTTPException(status_code=404, detail="Flex message not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user.put("/api/flexmessage/{message_id}")
async def update_flex_message(message_id: str, data: Flexmessage):
    try:
        code_dict = data.dict()

        result = collection.update_one(
            {"id": message_id}, {"$set": code_dict})

        if result.modified_count > 0:
            updated_data = collection.find_one({"id": message_id})
            serialized_data = flexmessages_serializer([updated_data])
            return {"status": "Ok", "data": serialized_data}
        else:
            raise HTTPException(status_code=404, detail="Flex message not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@user.delete("/api/flexmessage/{message_id}")
async def delete_flex_message(message_id: str):
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
        
        return {"status": "Ok", "message": serialized_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





# @user.post("/")
# async def create_flex_message(data: Flexmessage):
#     code_dict = data.dict()
#     id = collection.insert_one(code_dict)
#     # Read the newly inserted data from the database
#     inserted_id = collection.insert_one(id.dict()).inserted_id
#     # Serialize the data into the desired format
#     # serialized_data = flexmessages_serializer([inserted_data])
#     return {"status": "Success", }


# async def create_upload_file(file: UploadFile = File(...),name: str = "", category: str = "", code: Dict[str, Any] = "", status: bool = False):
#     file.filename = f"{uuid.uuid4()}.jpg"
#     contents = await file.read()

#         # Save the Flexmessage object or perform other operations
#     with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
#         f.write(contents)

#     # Save the file
#     with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
#         f.write(contents)
#     # Create the Flexmessage object
#     flex_message = Flexmessage(
#         name=name,
#         category=category,
#         photo=file.filename,  # กำหนดชื่อไฟล์ภาพที่ต้องการ
#         code=code,
#         status=status
#     )

#     data = collection.insert_one(flex_message.c)
#     # Read the newly inserted data from the database
#     return {"status": "Success"}
