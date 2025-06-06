from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db  
from app.schemas import user_schema 
from app.models import user_model

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/", response_model=user_schema.User)
def create_user(request: user_schema.User, db: Session = Depends(get_db)):
    db_user = user_model.User(
        name=request.name,
        username=request.username,
        password=request.password,  
        dob=request.dob,
        gender=request.gender
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{id}", response_model=user_schema.User)
def show_user(id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    return user

@router.delete("/{id}", response_model=user_schema.User)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    db.delete(user)
    db.commit()
    return user


@router.put("/{id}", response_model=user_schema.User)
def update_user(id: int,request:user_schema.User, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    user.name = request.name
    user.username = request.username
    user.password = request.password 
    user.dob = request.dob
    user.gender = request.gender
    
    db.commit() 
    db.refresh(user)
    return user