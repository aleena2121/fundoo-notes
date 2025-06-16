from app.auth.oauth2 import get_current_user
from app.models.labels_model import Labels as label_model
from app.schemas.labels_schema import Label as label_schema
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.exceptions import LabelAlreadyExistsException
from app.config.logger import func_logger


label_router = APIRouter(tags=["Labels"], prefix="/labels")


@label_router.post("/")
def create_label(
    request: label_schema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if (
        db.query(label_model)
        .filter(
            label_model.title == request.title, label_model.user_id == current_user.id
        )
        .first()
    ):
        raise LabelAlreadyExistsException(request.title)
    new_label = label_model(**request.model_dump())
    new_label.user_id = current_user.id
    db.add(new_label)
    db.commit()
    db.refresh(new_label)
    func_logger.info(f"Label with title {request.title} created.")
    return {
        "message": "Label created",
        "payload": new_label,
        "status_code": status.HTTP_201_CREATED,
    }


@label_router.get("/")
def show_all_labels(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    labels = db.query(label_model).filter(label_model.user_id == current_user.id).all()
    if not labels:
        return {
            "message": "No Labels Found",
            "payload": "",
            "status_code": status.HTTP_404_NOT_FOUND,
        }
    return {
        "message": "Labels Found",
        "payload": labels,
        "status_code": status.HTTP_201_CREATED,
    }


@label_router.put("/{id}")
def update_label(
    request: label_schema,
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    label = (
        db.query(label_model)
        .filter(label_model.id == id, label_model.user_id == current_user.id)
        .first()
    )
    if not label:
        return {
            "message": "No Labels Found",
            "payload": "",
            "status_code": status.HTTP_404_NOT_FOUND,
        }

    updated_data = request.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(label, key, value)

    db.commit()
    db.refresh(label)

    func_logger.info(f"Label with id {id} updated")

    return {
        "message": "Label Updated",
        "payload": label,
        "status_code": status.HTTP_201_CREATED,
    }


@label_router.delete("/{id}")
def delete_label(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    label = (
        db.query(label_model)
        .filter(label_model.id == id, label_model.user_id == current_user.id)
        .first()
    )
    if not label:
        return {
            "message": "No Label Found",
            "payload": "",
            "status_code": status.HTTP_404_NOT_FOUND,
        }

    db.delete(label)
    db.commit()

    func_logger.info(f"Label with id {id} deleted")

    return {
        "message": "Labels Found",
        "payload": "",
        "status_code": status.HTTP_200_OK,
    }
