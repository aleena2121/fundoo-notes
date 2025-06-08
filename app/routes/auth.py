from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.token import AccessToken
from app.database import get_db
from app.models import user_model
from app.utils.exceptions import InvalidCredentialsException
from app.utils.hashing import Hash

router = APIRouter(
    tags=['Auth']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.username == request.username).first()
    if not user or not Hash.verify(request.password, user.password):
        raise InvalidCredentialsException()
    
    access_token = AccessToken.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}