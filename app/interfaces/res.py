from app.dependencies import typing
from app.dependencies import generics
from app.dependencies import pydantic

T = generics.TypeVar('T', bound=pydantic.BaseModel)

class Res(generics.GenericModel, typing.Generic[T]):
    success: bool
    body: typing.Optional[T]
    message: typing.Optional[str] = pydantic.Field(example='error message')
