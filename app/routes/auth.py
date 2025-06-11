from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth.token import AccessToken
from app.config.logger import func_logger
from app.database import get_db
from app.models import user_model
from app.schemas import user_schema
from app.utils.exceptions import (DatabaseIntegrityError,
                                  InvalidCredentialsException,
                                  TokenCreationError,
                                  UsernameAlreadyExistsException)
from app.utils.generate_key import generate_key
from app.utils.hashing import Hash
from app.utils.email_verification import generate_verification_token, verify_email_token
from app.utils.email import send_verification_email

login_router = APIRouter(tags=['Login'])
sign_up_router = APIRouter(tags=['SignUp'])


@login_router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(user_model.User).filter(
            user_model.User.username == request.username
        ).first()

        if not user or not Hash.verify(request.password, user.password):
            raise InvalidCredentialsException()

        try:
            token_obj = AccessToken(time_expire=30, secret_key=user.secret_key)
            access_token = token_obj.create_access_token(data={"sub": user.username})
            func_logger.info("User Logged in")
            return {"access_token": access_token, "token_type": "bearer"}
        except Exception:
            raise TokenCreationError(detail="Failed to generate authentication token")

    except SQLAlchemyError:
        raise DatabaseIntegrityError(detail="Database error during login")


@sign_up_router.post("/signup")
async def sign_up(request: user_schema.User, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if db.query(user_model.User).filter(
        user_model.User.username == request.username
    ).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    secret_key = generate_key(request.username)
    
    new_user = user_model.User(
        name=request.name,
        username=request.username,
        password=Hash.bcrypt(request.password),
        dob=request.dob,
        gender=request.gender,
        secret_key=secret_key,
        is_verified=False
    )
    
   
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    verification_token = generate_verification_token(
        username=new_user.username,
        secret_key=new_user.secret_key
    )
    
    background_tasks.add_task(
        send_verification_email,
        email=new_user.username,
        token=verification_token
    )
    
    return {"message": "Verification email sent"}

@sign_up_router.get("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    result = verify_email_token(token, db)
    
    if result["status"] == "verified":
        return {"message": "Email verification successful! You can now login.", "username": result["user"].username}
    else:
        raise HTTPException(status_code=400, detail="Verification failed")