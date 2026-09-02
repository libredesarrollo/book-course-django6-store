from ninja import Schema
from typing import Optional
from datetime import datetime


class CategorySchema(Schema):
    id: int
    title: str
    slug: str


class TypeSchema(Schema):
    id: int
    title: str
    slug: str


class CommentSchema(Schema):
    id: int
    text: str
    date_posted: datetime
    element: Optional[int] = None
    count: int


class ElementReadSchema(Schema):
    id: int
    title: str
    slug: str
    description: str
    price: float
    created: datetime
    updated: datetime
    category: CategorySchema
    type: TypeSchema


class ElementWriteSchema(Schema):
    title: str
    slug: str = ""
    description: str
    price: float = 6.10
    category: int
    type: int


class TodoSchema(Schema):
    id: int
    name: str
    status: bool


class TodoCreateSchema(Schema):
    name: str
    status: bool = False


class SortSchema(Schema):
    ids: str


class LoginSchema(Schema):
    username: str
    password: str


class TokenSchema(Schema):
    token: str
