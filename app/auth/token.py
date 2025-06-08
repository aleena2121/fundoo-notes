from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.config import settings
from app.schemas import token_schema


class AccessToken:
    def __init__(self, algorithm="HS256", time_expire=30, secret_key=None):
        self.algorithm = algorithm
        self.time_expire = time_expire
        self.secret_key = settings.SECRET_KEY
        
    @staticmethod    
    def create_access_token(data: dict, expires_delta: timedelta|None=None, algorithm="HS256", time_expire=30, secret_key=None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=time_expire)

        to_encode.update({"exp": expire})
        
        key = secret_key or settings.SECRET_KEY
        encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm)
        return encoded_jwt

    def verify_access_token(self, token: str, credentials_exception):
        try:
            header = jwt.get_unverified_header(token)
            algo = header.get("alg", self.algorithm)
            
            payload = jwt.decode(token, self.secret_key, algorithms=[algo])
            username = payload.get("sub")
            if username is None: 
                raise credentials_exception
            
            token_data = token_schema.TokenData(username=username, secret_key=self.secret_key)
        
        except JWTError:
            raise credentials_exception
        
        return token_data