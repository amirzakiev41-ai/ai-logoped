from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int = Field(ge=0)
    user_name: str = Field(min_length=3, max_length=15)
    email: EmailStr


class CreateUserRequest(BaseModel):
    user_name: str = Field(min_length=3, max_length=15)
    email: EmailStr


class UpdateUserRequest(BaseModel):
    user_name: str = Field(min_length=3, max_length=15)


class AllUsersResponse(BaseModel):
    all_users: list[UserResponse]


class MessageResponse(BaseModel):
    message: str


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    
    user_name: str = Field(min_length=3, max_length=15)
    password: bytes
    email: EmailStr
    active: bool