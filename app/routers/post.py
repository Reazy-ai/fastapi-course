from fastapi import HTTPException, APIRouter, status
from fastapi.params import Depends
from sqlalchemy import func
from sqlmodel import select, update
from typing import List, Annotated, Optional

from app import schemas, models, oauth2
from app.database import SessionDep

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: SessionDep, current_user: Annotated[int, Depends(oauth2.get_current_user)]):

    statement = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
    )

    posts = db.exec(statement).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: SessionDep,
                current_user: Annotated[int, Depends(oauth2.get_current_user)]):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: SessionDep, current_user: Annotated[int, Depends(oauth2.get_current_user)]):
    statement = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id).where(models.Post.id == post_id)
    )
    post = db.exec(statement).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found")
    return post


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.CreatePost, db: SessionDep,
                current_user: Annotated[str, Depends(oauth2.get_current_user)]):
    old_post = db.get(models.Post, post_id)
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if old_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized request")
    db.exec(update(models.Post).where(models.Post.id == post_id).values(post.model_dump()))
    db.commit()
    db.refresh(old_post)
    return old_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: SessionDep, current_user: Annotated[int, Depends(oauth2.get_current_user)]):
    deleted_post = db.get(models.Post, post_id)
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized request")
    db.delete(deleted_post)
    db.commit()
