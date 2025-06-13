from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth.token import AccessToken
from app.config.logger import func_logger
from app.database import get_db
from app.models import user_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        unverified = jwt.decode(token, key="", options={"verify_signature": False})
        username = unverified.get("sub")
        if not username:
            raise credentials_exception

        user = (
            db.query(user_model.User)
            .filter(user_model.User.username == username)
            .first()
        )
        if not user:
            raise credentials_exception

        token_obj = AccessToken(secret_key=user.secret_key)
        token_data = token_obj.verify_access_token(token, credentials_exception)
        return user

    except JWTError as e:
        func_logger.error({e})
        print(f"JWT Error in get_current_user: {e}")
        raise credentials_exception
