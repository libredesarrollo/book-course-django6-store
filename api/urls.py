from django.urls import path
from rest_framework import routers
from .viewsets import ElementReadOnlyViewSet, ElementCreateUpdateDestroyViewSet,  CategoryViewSet, TypeViewSet, CommentViewSet
route = routers.SimpleRouter()
# route.register('element',ElementReadOnlyViewSet, basename='element-lecture')
route.register('element',ElementCreateUpdateDestroyViewSet, basename='element-write')
route.register('category',CategoryViewSet)
route.register('type',TypeViewSet)
route.register('comment',CommentViewSet)
urlpatterns = route.urls