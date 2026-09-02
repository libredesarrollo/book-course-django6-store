from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from ninja import NinjaAPI, Query
from ninja.responses import Response
from ninja.security import HttpBearer

from rest_framework.authtoken.models import Token

from elements.models import Element, Category, Type
from comments.models import Comment
from todo.models import Todo

from .schemas import (
    CategorySchema, TypeSchema, CommentSchema,
    ElementReadSchema, ElementWriteSchema,
    TodoSchema, TodoCreateSchema, SortSchema,
    LoginSchema, TokenSchema,
)


class TokenAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            return Token.objects.select_related("user").get(key=token).user
        except Token.DoesNotExist:
            return None


api = NinjaAPI(
    title="MyStore Ninja API",
    version="1.0.0",
    auth=TokenAuth(),
)


# ──────────────────────────────────────────────
#  Elements (lectura)
# ──────────────────────────────────────────────
@api.get("/elements-read/", response=list[ElementReadSchema], tags=["elements-read"], auth=None)
def list_elements_read(request):
    return Element.objects.select_related("category", "type").all()


@api.get("/elements-read/{int:pk}/", response=ElementReadSchema, tags=["elements-read"], auth=None)
def get_element_read(request, pk: int):
    return get_object_or_404(
        Element.objects.select_related("category", "type"),
        pk=pk,
    )


# ──────────────────────────────────────────────
#  Elements (escritura)
# ──────────────────────────────────────────────
@api.post("/elements-write/", response=ElementReadSchema, tags=["elements-write"], auth=None)
def create_element(request, payload: ElementWriteSchema):
    data = payload.dict()
    element = Element.objects.create(**data)
    return get_object_or_404(
        Element.objects.select_related("category", "type"),
        pk=element.pk,
    )


@api.put("/elements-write/{int:pk}/", response=ElementReadSchema, tags=["elements-write"], auth=None)
def update_element(request, pk: int, payload: ElementWriteSchema):
    element = get_object_or_404(Element, pk=pk)
    for attr, value in payload.dict().items():
        setattr(element, attr, value)
    element.save()
    return get_object_or_404(
        Element.objects.select_related("category", "type"),
        pk=element.pk,
    )


@api.delete("/elements-write/{int:pk}/", tags=["elements-write"], auth=None)
def delete_element(request, pk: int):
    element = get_object_or_404(Element, pk=pk)
    element.delete()
    return {"detail": "Deleted"}


# ──────────────────────────────────────────────
#  Category
# ──────────────────────────────────────────────
@api.get("/category/", response=list[CategorySchema], tags=["category"], auth=None)
def list_categories(request):
    return Category.objects.all()


@api.post("/category/", response=CategorySchema, tags=["category"], auth=None)
def create_category(request, payload: CategorySchema):
    data = payload.dict()
    if data.get("title") and not data.get("slug"):
        data["slug"] = slugify(data["title"])
    return Category.objects.create(**data)


@api.get("/category/{int:pk}/", response=CategorySchema, tags=["category"], auth=None)
def get_category(request, pk: int):
    return get_object_or_404(Category, pk=pk)


@api.put("/category/{int:pk}/", response=CategorySchema, tags=["category"], auth=None)
def update_category(request, pk: int, payload: CategorySchema):
    category = get_object_or_404(Category, pk=pk)
    for attr, value in payload.dict().items():
        setattr(category, attr, value)
    category.save()
    return category


@api.delete("/category/{int:pk}/", tags=["category"], auth=None)
def delete_category(request, pk: int):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return {"detail": "Deleted"}


@api.get("/category/{int:pk}/elements/", response=list[ElementReadSchema], tags=["category"], auth=None)
def category_elements(request, pk: int):
    get_object_or_404(Category, pk=pk)
    return Element.objects.select_related("category", "type").filter(category_id=pk)


@api.get("/category/all/", response=list[CategorySchema], tags=["category"], auth=None)
def all_categories(request):
    return Category.objects.all()


@api.get("/category/url/", response=CategorySchema, tags=["category"], auth=None)
def category_by_slug(request, slug: str = Query(...)):
    return get_object_or_404(Category, slug=slug)


# ──────────────────────────────────────────────
#  Type
# ──────────────────────────────────────────────
@api.get("/type/", response=list[TypeSchema], tags=["type"], auth=None)
def list_types(request):
    return Type.objects.all()


@api.post("/type/", response=TypeSchema, tags=["type"], auth=None)
def create_type(request, payload: TypeSchema):
    return Type.objects.create(**payload.dict())


@api.get("/type/{int:pk}/", response=TypeSchema, tags=["type"], auth=None)
def get_type(request, pk: int):
    return get_object_or_404(Type, pk=pk)


@api.put("/type/{int:pk}/", response=TypeSchema, tags=["type"], auth=None)
def update_type(request, pk: int, payload: TypeSchema):
    type_obj = get_object_or_404(Type, pk=pk)
    for attr, value in payload.dict().items():
        setattr(type_obj, attr, value)
    type_obj.save()
    return type_obj


@api.delete("/type/{int:pk}/", tags=["type"], auth=None)
def delete_type(request, pk: int):
    type_obj = get_object_or_404(Type, pk=pk)
    type_obj.delete()
    return {"detail": "Deleted"}


@api.get("/type/all/", response=list[TypeSchema], tags=["type"], auth=None)
def all_types(request):
    return Type.objects.all()


# ──────────────────────────────────────────────
#  Comment
# ──────────────────────────────────────────────
@api.get("/comment/", response=list[CommentSchema], tags=["comment"], auth=None)
def list_comments(request):
    return Comment.objects.exclude(element__isnull=True)


@api.post("/comment/", response=CommentSchema, tags=["comment"], auth=None)
def create_comment(request, payload: CommentSchema):
    data = payload.dict()
    data.pop("count", None)
    comment = Comment.objects.create(**data)
    count = Comment.objects.filter(element_id=comment.element_id).count()
    return {**CommentSchema.from_orm(comment).dict(), "count": count}


@api.get("/comment/{int:pk}/", response=CommentSchema, tags=["comment"], auth=None)
def get_comment(request, pk: int):
    comment = get_object_or_404(Comment, pk=pk)
    count = Comment.objects.filter(element_id=comment.element_id).count()
    return {**CommentSchema.from_orm(comment).dict(), "count": count}


@api.put("/comment/{int:pk}/", response=CommentSchema, tags=["comment"], auth=None)
def update_comment(request, pk: int, payload: CommentSchema):
    comment = get_object_or_404(Comment, pk=pk)
    data = payload.dict()
    data.pop("count", None)
    for attr, value in data.items():
        setattr(comment, attr, value)
    comment.save()
    count = Comment.objects.filter(element_id=comment.element_id).count()
    return {**CommentSchema.from_orm(comment).dict(), "count": count}


@api.delete("/comment/{int:pk}/", tags=["comment"], auth=None)
def delete_comment(request, pk: int):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return {"detail": "Deleted"}


# ──────────────────────────────────────────────
#  Todo (requiere autenticación)
# ──────────────────────────────────────────────
@api.get("/todo/", response=list[TodoSchema], tags=["todo"])
def list_todos(request):
    return Todo.objects.filter(user=request.auth).order_by("count")


@api.post("/todo/", response=TodoSchema, tags=["todo"])
def create_todo(request, payload: TodoCreateSchema):
    count = Todo.objects.filter(user=request.auth).count()
    todo = Todo.objects.create(user=request.auth, count=count, **payload.dict())
    return todo


@api.get("/todo/{int:pk}/", response=TodoSchema, tags=["todo"])
def get_todo(request, pk: int):
    return get_object_or_404(Todo, pk=pk, user=request.auth)


@api.put("/todo/{int:pk}/", response=TodoSchema, tags=["todo"])
def update_todo(request, pk: int, payload: TodoCreateSchema):
    todo = get_object_or_404(Todo, pk=pk, user=request.auth)
    for attr, value in payload.dict().items():
        setattr(todo, attr, value)
    todo.save()
    return todo


@api.delete("/todo/{int:pk}/", tags=["todo"])
def delete_todo(request, pk: int):
    todo = get_object_or_404(Todo, pk=pk, user=request.auth)
    todo.delete()
    return {"detail": "Deleted"}


@api.post("/todo/sort/", tags=["todo"])
def sort_todos(request, payload: SortSchema):
    ids = payload.ids.split(",")
    for i, todo_id in enumerate(ids):
        Todo.objects.filter(user=request.auth, id=todo_id).update(count=i)
    return {"detail": "OK"}


@api.delete("/todo/delete-all/", tags=["todo"])
def delete_all_todos(request):
    Todo.objects.filter(user=request.auth).delete()
    return {"detail": "OK"}


# ──────────────────────────────────────────────
#  Login
# ──────────────────────────────────────────────
@api.post("/login/", response=TokenSchema, tags=["auth"], auth=None)
def login(request, payload: LoginSchema):
    try:
        user = User.objects.get(username=payload.username)
    except User.DoesNotExist:
        return Response({"detail": "User is invalid"}, status=400)

    if not check_password(payload.password, user.password):
        return Response({"detail": "Password is invalid"}, status=400)

    token, _ = Token.objects.get_or_create(user=user)
    return {"token": token.key}
