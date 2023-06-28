
# message code item
def flexmessage_serializer(data) -> dict:
    return {
        "type": data.get("code_flexmessage").get("type"),
        "header": data.get("code_flexmessage").get("header"),
        "hero": data.get("code_flexmessage").get("hero"),
        "body": data.get("code_flexmessage").get("body"),
        "footer": data.get("code_flexmessage").get("footer")
    }

# message all item


def flexmessages_serializer(datas) -> list:
    return [flexmessage_serializer(data) for data in datas]


def data_serializer(data) -> dict:
    return {
        "id": data["id"],
        "name": data["name"],
        "category": data["category"],
        "photo": data["photo"],
        "code_flexmessage": data["code_flexmessage"],
        "status": data["status"]
    }


def datas_serializer(datas) -> list:
    return [data_serializer(data) for data in datas]
