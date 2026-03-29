from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    is_active: bool = True


class UserInDB(UserModel):
    id: str = Field(alias="_id")
