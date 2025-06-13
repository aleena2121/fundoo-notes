from fastapi import HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth.token import AccessToken
from app.database import get_db
from app.models import user_model


def generate_verification_token(username: str, secret_key: str) -> str:
    token_obj = AccessToken(time_expire=15, secret_key=secret_key)
    return token_obj.create_access_token(data={"sub": username})


def verify_email_token(token: str, db: Session) -> dict:
    try:
        payload = jwt.decode(token, key=None, options={"verify_signature": False})
        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=400, detail="Invalid token structure")

        user = (
            db.query(user_model.User)
            .filter(user_model.User.username == username)
            .first()
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            jwt.decode(token, key=user.secret_key, algorithms=["HS256"])
        except JWTError as e:
            error_msg = str(e).lower()
            if "expired" in error_msg or "signature has expired" in error_msg:
                raise HTTPException(status_code=400, detail="Token has expired")
            else:
                raise HTTPException(status_code=400, detail="Invalid token")

        user.is_verified = True
        db.commit()

        return {"status": "verified", "user": user}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Verification failed: {str(e)}")
