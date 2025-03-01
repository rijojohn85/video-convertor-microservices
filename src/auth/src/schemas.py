from pydantic import BaseModel, Field, UUID4


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=6)


class UserInDBSchema(BaseModel):
    id: UUID4
    username: str
