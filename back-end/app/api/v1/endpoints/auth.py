from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# use a relative import so the local v1 package resolves correctly in editors and at runtime
from ..dependencies import get_db
from app.core import auth as auth_core
from app import crud
from app.schemas.user import Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.user.get_by_email(db, form_data.username)
    if not user or not auth_core.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    access_token = auth_core.create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}