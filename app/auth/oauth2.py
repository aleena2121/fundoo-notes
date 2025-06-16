from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.models import user_model
from app.utils.redis_client import r
from app.config.logger import func_logger
from app.auth.token import AccessToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def rate_limit_user(user_id: int, limit: int = 20, window: int = 60):
    current_window = int(datetime.now().timestamp() // window)
    redis_key = f"rate_limit:user:{user_id}:{current_window}"

    current = r.incr(redis_key)
    if current == 1:
        r.expire(redis_key, window)

    if current > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many requests, Try after some time",
        )


async def get_current_user(
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

        await rate_limit_user(user.id)

        return user

    except JWTError as e:
        func_logger.error(f"JWT Error in get_current_user: {e}")
        raise credentials_exception
