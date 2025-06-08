from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.auth.token import AccessToken
from app.database import get_db
from app.models import user_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token_data: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate the user",
        headers={"WWW-Authenticate": "Bearer"}        
    )
    
    try:
        tokenobj = AccessToken()
        token_payload = tokenobj.verify_access_token(token_data, credentials_exception)
        
        username = token_payload.username
        
        user = db.query(user_model.User).filter(user_model.User.username == username).first()
        if not user:
            raise credentials_exception
            
        return user
        
    except JWTError:
        raise credentials_exception