from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.models import user_model
from app.schemas import user_schema
from app.utils.exceptions import UsernameAlreadyExistsException, UserNotFoundException
from app.utils.hashing import Hash

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.ShowUser)
def create_user(request: user_schema.User, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    existing_username = db.query(user_model.User).filter(user_model.User.username == request.username).first()
    if existing_username:
        raise UsernameAlreadyExistsException()
    user_data = request.model_dump()
    user_data["password"] = Hash.bcrypt(request.password)
    new_user = user_model.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=user_schema.ShowUser)
def get_user(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()
    if not user:
        raise UserNotFoundException(user_id=id)
    return user


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_details(
    id: int, request: user_schema.UpdateUser, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(user_model.User).filter(user_model.User.id == id)
    if not user.first():
        raise UserNotFoundException(user_id=id)
    update_data = request.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = Hash.bcrypt(update_data["password"])
    user.update(update_data)
    db.commit()
    return {"message": "User Details updated!!"}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = db.query(user_model.User).filter(user_model.User.id == id)
    if not user.first():
        raise UserNotFoundException(user_id=id)
    user.delete(synchronize_session=False)
    db.commit()
    return {"message": "User Deleted!!"}