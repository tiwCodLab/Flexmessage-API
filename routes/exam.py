from fastapi import APIRouter
from models.flexaver_models import Code, Flexmessage
from schemas.flexaver_schema import users_serializer
from bson import ObjectId
from config.db import collection
import json


user = APIRouter()


# @user.post("/")
# async def create_user(data: Flexmessage):
#     _id = collection.insert_one(dict(data))
#     data = users_serializer(list(collection.find({"_id": _id.inserted_id})))
#     return {"status": "Ok", "data": data}

@user.post("/")
async def create_flexmassage(data: Flexmessage):
    code_dict = json.loads(data.code)
    data.code = Code(**code_dict)

    _id = collection.insert_one(data.dict())
    data = users_serializer(list(collection.find({"_id": _id.inserted_id})))
    return {"status": "Ok", "data": data}


@user.get("/")
async def find_all_flexmassage():
    datas = users_serializer(list(collection.find()))
    return {"status": "Ok", "data": datas}


@user.get("/{id}")
async def get_one_flexmassage(id: str):
    data = users_serializer(collection.find({"_id": ObjectId(id)}))
    return {"status": "Ok", "data": data}


@user.put("/{id}")
async def update_flexmassage(id: str, updated_user: Flexmessage):
    updated_user_data = dict(updated_user)
    collection.find_one_and_update({"_id": ObjectId(id)}, {
                                   "$set": updated_user_data})
    user = users_serializer(collection.find({"_id": ObjectId(id)}))
    return {"status": "Ok", "data": user}


@user.delete("/{id}")
async def delete_flexmassage(id: str):
    collection.find_one_and_delete({"_id": ObjectId(id)})
    users = users_serializer(collection.find())
    return {"status": "Ok", "data": []}
