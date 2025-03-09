from fastapi import HTTPException, APIRouter, status

from app import schemas, models
from app.database import SessionDep
from app.oauth2 import UserDep

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: SessionDep, current_user: UserDep):
    post_exist = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already voted on this post")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}