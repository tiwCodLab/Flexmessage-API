from fastapi import APIRouter,HTTPException,Body
from models.flexaver_models import Flexmessage ,CodeDict
from schemas.flexaver_schema import flexmessages_serializer, datas_serializer
from config.db import collection
user = APIRouter()


current_id = 0
@user.post("/api/")
async def create_flexmessage(name: str = Body(...), category: str = Body(...), code_flexmessage: CodeDict = Body(...), status: bool = Body(False)):
    global current_id
    try:
        # Create the data to be inserted
        flex_message = Flexmessage(
            name=name,
            category=category,
            code_flexmessage=code_flexmessage.dict(exclude_unset=True),
            status=status,
            id=current_id + 1
        )
        current_id += 1
        # Insert data into the database
        inserted_id = collection.insert_one(flex_message.dict()).inserted_id
        return {"status": "Success"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user.post("/api/flexmessage/")
async def create_flex_message(name: str = Body(...), category: str = Body(...), code_flexmessage: CodeDict = Body(...), status: bool = Body(False)):
    try:
        # Get the current counter value from the database
        latest_document = collection.find().sort('_id', -1).limit(1).next()
        current_counter = latest_document['id']
        # Increment the counter
        new_counter = current_counter + 1
        # Update the counter value in the database
        # collection.update_one({}, {'$set': {'id': new_counter}})
        # Create the data to be inserted
        flex_message = Flexmessage(
            name=name,
            category=category,
            code_flexmessage=code_flexmessage.dict(exclude_unset=True),
            status=status,
            id=new_counter
        )
        # Insert data into the database
        inserted_id = collection.insert_one(flex_message.dict()).inserted_id
        return {"status": "Success"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



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



