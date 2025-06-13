from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.config import settings
from app.config.logger import config_logger, func_logger, logger
from app.schemas import token_schema


class AccessToken:
    def __init__(self, algorithm="HS256", time_expire=30, secret_key=None):
        self.algorithm = algorithm
        self.time_expire = time_expire
        self.secret_key = secret_key or settings.SECRET_KEY

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.time_expire)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_access_token(self, token: str, credentials_exception):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            func_logger.info("User Authenticated")

            return token_schema.TokenData(username=username)

        except JWTError as e:
            print(f"JWT Error: {e}")
            raise credentials_exception
