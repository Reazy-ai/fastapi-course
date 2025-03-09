from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from app import models, utils
from app import database, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: database.SessionDep):
    statement = select(models.User).where(models.User.email == user_credentials.username)
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
