from app.celery_app import celery_app
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session, selectinload
from app.database import SessionLocal
from app.utils.email import send_expiration_email
from app.config.logger import func_logger
from app.models.notes_model import Notes
from app.models.user_model import User
from app.utils.redis_client import set_cache


@celery_app.task
def notify_and_cleanup_notes():
    func_logger.info("Note expiration task started")
    db: Session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)

        next_24h = now + timedelta(hours=24)
        expiring_soon = (
            db.query(Notes)
            .options(selectinload(Notes.creator))
            .filter(Notes.expiry_date >= now, Notes.expiry_date <= next_24h)
            .all()
        )
        func_logger.info(f"Found {len(expiring_soon)} notes expiring soon")

        for note in expiring_soon:
            try:
                user_email = note.creator.username
                link = f"http://localhost:8000/notes/extend-expiry/{note.id}"
                send_expiration_email(
                    user_email,
                    "Your note is about to expire",
                    f"Your note will expire soon. Click here to extend it: {link}",
                )
                func_logger.info(f"Sent expiration warning to {user_email}")
            except Exception as e:
                func_logger.error(f"Failed to send email for note {note.id}: {str(e)}")

        expired_notes = db.query(Notes).filter(Notes.expiry_date < now).all()

        if expired_notes:
            func_logger.info(f"Found {len(expired_notes)} expired notes to delete")
            for note in expired_notes:
                db.delete(note)
                func_logger.info(f"Deleted expired note ID {note.id}")
            db.commit()

    except Exception as e:
        func_logger.error(f"Task failed: {str(e)}")
        db.rollback()
    finally:
        db.close()


@celery_app.task
def refresh_recent_notes_cache():
    db: Session = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            notes = (
                db.query(Notes)
                .filter(Notes.user_id == user.id)
                .order_by(Notes.created_at.desc())
                .limit(10)
                .all()
            )

            serialized_notes = [
                {
                    "id": note.id,
                    "title": note.title,
                    "content": note.content,
                    "created_at": note.created_at.isoformat(),
                    "expiry_date": note.expiry_date.isoformat(),
                    "labels": [label.title for label in note.labels],
                }
                for note in notes
            ]

            set_cache(
                key=f"recent_notes_user_{user.id}",
                value=serialized_notes,
                expire_seconds=1200,
            )
    finally:
        db.close()
