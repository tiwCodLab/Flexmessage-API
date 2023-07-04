from pydantic import BaseModel, Field
from typing import Any, Dict
from datetime import datetime


class Flexmessage(BaseModel):
    id: int
    name: str = None
    category: str = None
    photo: str = None
    code_flexmessage: Dict[str, Any] = None
    status: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# เป็นโค้ด json ของ message
class CodeDict(BaseModel):
    type: str = None
    direction: str = None
    size: str = None
    header: dict = None
    hero: dict = None
    contents: object = None
    body: dict = None
    styles: dict = None
    footer: dict = None


# class Flexmessage(BaseModel):
#     id: str = Field(default_factory=lambda: str(uuid.uuid4()))
#     name: str = None
#     category: str = None
#     photo: str = None
#     code_flexmessage:  Dict[str, Any] = None
#     status: bool = Field(default=False)
#     created_at: datetime = Field(default_factory=datetime.utcnow)
