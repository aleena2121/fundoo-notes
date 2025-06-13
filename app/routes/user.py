from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.config.logger import config_logger, func_logger
from app.database import get_db
from app.models import user_model
from app.schemas import user_schema
from app.utils.exceptions import (
    DatabaseIntegrityError,
    PermissionDeniedException,
    UserNotFoundException,
)
from app.utils.hashing import Hash

router = APIRouter(prefix="/user", tags=["Users"])


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=user_schema.ShowUser
)
def get_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(user_model.User).filter(user_model.User.id == id).first()
        if not user:
            config_logger.error(f"User with id {id} not found")
            raise UserNotFoundException(user_id=id)
        func_logger.info("User found")
        return user
    except SQLAlchemyError as e:
        config_logger.error("DB Connection Error")
        raise DatabaseIntegrityError(detail=str(e))


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_details(
    id: int,
    request: user_schema.UpdateUser,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        user = db.query(user_model.User).filter(user_model.User.id == id).first()
        if not user:
            func_logger.error(f"User with id {id} not found")
            raise UserNotFoundException(user_id=id)
        if current_user.id != user.id:
            func_logger.error("Permission denied")
            raise PermissionDeniedException()

        update_data = request.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = Hash.bcrypt(update_data["password"])

        db.query(user_model.User).filter(user_model.User.id == id).update(update_data)
        db.commit()
        func_logger.info(f"User with id {id} updated")
        return {"message": f"User Details for id {id} updated successfully"}

    except IntegrityError:
        config_logger.error("Data conflict error, rolling back!")
        db.rollback()
        raise DatabaseIntegrityError(detail="Data conflict occurred")
    except SQLAlchemyError:
        db.rollback()
        config_logger.error("Database operation failed, rolling back!")
        raise DatabaseIntegrityError(detail="Database operation failed")


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    try:
        user = db.query(user_model.User).filter(user_model.User.id == id).first()
        if not user:
            func_logger.error(f"User with id {id} not found")
            raise UserNotFoundException(user_id=id)
        if current_user.id != user.id:
            func_logger.error("Permission denied")
            raise PermissionDeniedException()
        func_logger.info(f"User with id {id} Deleted")
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}

    except SQLAlchemyError:
        config_logger.error("Database operation failed, rolling back!")
        db.rollback()
        raise DatabaseIntegrityError(detail="Failed to delete user")
