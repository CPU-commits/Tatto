from app.dependencies import pydantic
from app.dependencies import UserTypes

class TokenData(pydantic.BaseModel):
    user_type: UserTypes
    id: str
    sub: str
