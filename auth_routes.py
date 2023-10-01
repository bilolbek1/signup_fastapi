from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from database import Session, engine
from models import User
from schemas import SignUpModel, LoginModel
from fastapi.exceptions import HTTPException
from werkzeug.security import check_password_hash, generate_password_hash
import datetime


auth_router = APIRouter(
    prefix="/auth"
)

session = Session(bind=engine)


@auth_router.get("/")
async def hello(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")
    return {"message": "Hello SignUp Page"}




@auth_router.post("/signup")
async def signup(user: SignUpModel):
    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the username already exists")

    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the email already exists")


    new_user = User(
        username= user.username,
        email= user.email,
        password= generate_password_hash(user.password),
        is_staff= user.is_staff,
        is_active= user.is_active
    )

    session.add(new_user)
    session.commit()

    data = {
        "id":new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "password": new_user.password,
        "is_active": new_user.is_active,
        "is_staff": new_user.is_staff
    }

    return jsonable_encoder(data)




@auth_router.post('/login')
async def login(user: LoginModel, Authorize:AuthJWT=Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_limit_time = datetime.timedelta(seconds=20)
        refresh_limit_time = datetime.timedelta(days=5)

        access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_limit_time)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=refresh_limit_time)

        token = {
            "access": access_token,
            "refresh": refresh_token
        }

        data = {
            "success": True,
            "message": "Access token successfully created",
            "token": token
        }

        jsonable_encoder(data)


    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid username or password")









































































