from typing import Annotated

import jwt
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from sqlmodel import select
from .config import settings
from app import schemas, models
from app.database import SessionDep

oauth2_scheme = OAuth2PasswordBearer("login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        user_id: str = str(payload.get("user_id"))
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except PyJWTError:
        raise credentials_exception
    return token_data

def get_current_user(db: SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"}
                                         )
    token = verify_token(token, credentials_exception)
    user = db.exec(select(models.User).filter(models.User.id == int(token.id))).first()
    return user


UserDep = Annotated[int, Depends(get_current_user)]