from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator, field_validator


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass

class UserResponse(BaseModel):
    email: EmailStr
    id: int

    class Config:
        from_attributes = True

class Post(PostBase):
    created_at: datetime
    # owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(UserCreate):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: int

    @classmethod
    def validate_vote_value(self, value):
        if value not in (0, 1):
            raise ValueError("vote_value must be either 0 or 1")
        return value