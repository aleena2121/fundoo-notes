from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, selectinload

from app.auth.oauth2 import get_current_user
from app.database import get_db
from app.models import notes_model, labels_model
from app.schemas import notes_schema
from app.utils.exceptions import TitleAlreadyExistsException, LabelDoesNotExistException, LabelRequiredException
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
        .filter(notes_model.Notes.title == request.title,
            notes_model.Notes.user_id == current_user.id)
        .first()
    ):
        raise TitleAlreadyExistsException(request.title)
    
    if len(request.labels) == 0:
        raise LabelRequiredException()
    
    label_objs = db.query(labels_model.Labels).filter(
        labels_model.Labels.title.in_(request.labels),
        labels_model.Labels.user_id == current_user.id
    ).all()

    if len(label_objs) != len(request.labels):
        found_titles = {label.title for label in label_objs}
        missing = [l for l in request.labels if l not in found_titles]
        raise LabelDoesNotExistException(", ".join(missing))


    new_note = notes_model.Notes(**request.model_dump(exclude={"labels"}))
    new_note.user_id = current_user.id
    new_note.labels = label_objs
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    
    response_data = notes_schema.NotesResponse.model_validate(new_note)
    
    func_logger.info(f"Note with title {request.title} created.")
    return {
        "message": "Note created",
        "payload": response_data,
        "status_code": status.HTTP_201_CREATED,
    }


@notes_router.get("/")
def get_all_notes(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    notes = (
        db.query(notes_model.Notes)
        .options(selectinload(notes_model.Notes.labels))
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
        .options(selectinload(notes_model.Notes.labels))
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
    if hasattr(request, 'labels') and request.labels is not None:
        if len(request.labels) == 0:
            raise LabelRequiredException()
        
        label_objs = db.query(labels_model.Labels).filter(
            labels_model.Labels.title.in_(request.labels),
            labels_model.Labels.user_id == current_user.id
        ).all()

        if len(label_objs) != len(request.labels):
            found_titles = {label.title for label in label_objs}
            missing = [l for l in request.labels if l not in found_titles]
            raise LabelDoesNotExistException(", ".join(missing))
        
        note.labels = label_objs
    
    updated_note = request.model_dump(exclude_unset=True, exclude={"labels"})
    for key, value in updated_note.items():
        setattr(note, key, value)
    db.commit()
    func_logger.info(f"Note with id {id} updated")
    return {
        "message": f"Note updated successfully",
        "payload": note,
        "status_code": status.HTTP_200_OK,
    }
