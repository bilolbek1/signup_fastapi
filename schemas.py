from pydantic import BaseModel
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
    auth_jwt_secret_key: str = 'c87dcb38c9cb85f251531be840cddec9140210b9031304a1b59984bfda6cab70'



class LoginModel(BaseModel):
    username: str
    password: str












































































