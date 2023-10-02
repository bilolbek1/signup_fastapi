from pydantic import BaseModel, BaseSettings
from typing import Optional



class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]


    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "username": "string",
                "email": "string@gamil.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }




class Settings(BaseModel):
    auth_jwt_secret_key: str = '222fd4ddcabfbfa5e1c989d1bbbc5a02'




class LoginModel(BaseModel):
    username: str
    password: str












































































