from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from elements.models import Element, Category, Type
from comments.models import Comment

from .serializers import ElementReadOnlySerializer, ElementCreateUpdateDestroySerializer, CategorySerializer, TypeSerializer, CommentSerializer

# class ElementViewSet(viewsets.ModelViewSet):
#     queryset = Element.objects.all()
#     serializer_class = ElementSerializer
    
class ElementReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementReadOnlySerializer
    
class ElementCreateUpdateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Element.objects.all()
    serializer_class = ElementCreateUpdateDestroySerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    @action(detail=True, methods=['get'])
    def elements(self, request, pk=None):
        queryset = Element.objects.filter(category_id=pk)
        serializer = ElementReadOnlySerializer(queryset, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['get'])
    def all(self, request):
         queryset = Category.objects.all()
         serializer = CategorySerializer(queryset, many=True)
         return Response(serializer.data)
    @action(detail=False, methods=['get'])
    def url(self, request): # /api/category/url/?slug=some-slug
        if 'slug' in request.query_params:
            queryset = get_object_or_404(Category,slug=request.query_params['slug'])
            serializer = CategorySerializer(queryset, many=False)
            return Response(serializer.data)
        return Response({"detail": "Parameter 'slug' is required."}, status=400)


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.exclude(element__isnull=True)
    serializer_class = CommentSerializer