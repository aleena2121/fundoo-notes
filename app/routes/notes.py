from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.models import notes_model
from app.schemas import notes_schema
from app.utils.exceptions import TitleAlreadyExistsException
from app.config.logger import func_logger

notes_router = APIRouter(tags=["Notes"], prefix="/notes")


@notes_router.post("/")
def create_notes(
    request: notes_schema.Notes,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if (
        db.query(notes_model.Notes)
        .filter(notes_model.Notes.title == request.title)
        .first()
    ):
        raise TitleAlreadyExistsException(request.title)
    new_note = notes_model.Notes(**request.model_dump())
    new_note.user_id = current_user.id
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    func_logger.info(f"Note with title {request.title} created.")
    return {
        "message": "Note created",
        "payload": new_note,
        "status_code": status.HTTP_201_CREATED,
    }


@notes_router.get("/")
def get_all_note(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    notes = (
        db.query(notes_model.Notes)
        .filter(
            notes_model.Notes.user_id == current_user.id
        )
        .all()
    )
    if not notes:
        return {
            "message": f"No notes found",
            "payload": "",
            "status_code": status.HTTP_404_NOT_FOUND,
        }
    return {
        "message": f"Notes found",
        "payload": notes,
        "status_code": status.HTTP_200_OK,
    }


@notes_router.get("/{id}")
def get_note_by_id(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    note = (
        db.query(notes_model.Notes)
        .filter(
            notes_model.Notes.id == id, notes_model.Notes.user_id == current_user.id
        )
        .first()
    )
    if not note:
        return {
            "message": f"No note found with id : {id}",
            "payload": "",
            "status_code": status.HTTP_404_NOT_FOUND,
        }
    return {
        "message": f"Note found",
        "payload": note,
        "status_code": status.HTTP_200_OK,
    }


@notes_router.delete("/{id}")
def delete_note(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    note = (
        db.query(notes_model.Notes)
        .filter(
            notes_model.Notes.id == id, notes_model.Notes.user_id == current_user.id
        )
        .first()
    )
    if not note:
        return {
            "message": f"No note found with id : {id}",
            "payload": "",
            "status_code": status.HTTP_404_NOT_FOUND,
        }
    db.delete(note)
    db.commit()
    func_logger.info(f"Note with id {id} deleted")
    return {
        "message": f"Note deleted successfully",
        "payload": note,
        "status_code": status.HTTP_200_OK,
    }


@notes_router.put("/{id}")
def update_note(
    id: int,
    request: notes_schema.UpdateNote,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    note = (
        db.query(notes_model.Notes)
        .filter(
            notes_model.Notes.id == id, notes_model.Notes.user_id == current_user.id
        )
        .first()
    )
    if not note:
        return {
            "message": f"No note found with id : {id}",
            "payload": "",
            "status_code": status.HTTP_404_NOT_FOUND,
        }
    updated_note = request.model_dump(exclude_unset=True)
    for key, value in updated_note.items():
        setattr(note, key, value)
    db.commit()
    func_logger.info(f"Note with id {id} updated")
    return {
        "message": f"Note updated successfully",
        "payload": note,
        "status_code": status.HTTP_200_OK,
    }
