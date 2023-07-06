from pydantic import BaseModel, Field
from datetime import datetime


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


class Flexmessage(BaseModel):
    id: int = None
    name: str = None
    category: str = None
    image: str = None
    code_flexmessage: dict = Field(
        default_factory=lambda: CodeDict().dict(exclude_unset=True))
    status: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
