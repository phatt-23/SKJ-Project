from datetime import datetime
from typing import List
from ninja import Schema

# Create your models here.

# THESE ARE DTOs

# --- Repository ---

class RepositorySchema(Schema):
    id: int
    name: str
    owner: str  # username

    @classmethod
    def from_model(cls, r):
        return cls(id=r.id, name=r.name, owner=r.owner.username)


# --- File for Commit ---

class CommitFileSchema(Schema):
    path: str
    content: str


# --- Commit ---

class CommitSchema(Schema):
    id: int
    message: str
    timestamp: datetime
    repository: str  # repository name

    @classmethod
    def from_model(cls, c):
        return cls(id=c.id, message=c.message, timestamp=c.timestamp, repository=c.repository.name)


class CreateCommitSchema(Schema):
    message: str
    files: List[CommitFileSchema]


# --- Issue ---

class IssueSchema(Schema):
    id: int
    title: str
    description: str
    status: str
    created_by: str  # username
    created_at: datetime 

    @classmethod
    def from_model(cls, i):
        return cls(id=i.id, title=i.title, description=i.description, status=i.status, created_by=i.created_by.username, created_at=i.created_at)



class CreateIssueSchema(Schema):
    title: str
    description: str
    status: str  # open or closed


# --- Comment ---

class CommentSchema(Schema):
    id: int
    content: str
    author: str  # username
    created_at: datetime

    @classmethod
    def from_model(cls, c):
        return cls(
            id=c.id,
            content=c.content,
            author=c.author.username,
            created_at=c.created_at,
        )


class CreateCommentSchema(Schema):
    content: str


