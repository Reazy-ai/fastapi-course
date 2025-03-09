from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine
from .config import settings

databaseURL = (f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:'
               f'{settings.database_port}/{settings.database_name}')

engine = create_engine(databaseURL)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
