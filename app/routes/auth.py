from fastapi import APIRouter, Depends, status
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


@sign_up_router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.ShowUser)
def sign_up(request: user_schema.User, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(user_model.User).filter(
            user_model.User.username == request.username
        ).first()
        if existing_user:
            raise UsernameAlreadyExistsException(username=request.username)

        user_data = request.model_dump(exclude_unset=True)
        user_data["password"] = Hash.bcrypt(request.password)
        user_data["secret_key"] = generate_key(request.name)

        new_user = user_model.User(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except SQLAlchemyError:
        db.rollback()
        raise DatabaseIntegrityError(detail="Failed to create user")
