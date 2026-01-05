from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from elements.models import Element, Category, Type
from comments.models import Comment

from todo.models import Todo

from .serializers import ElementReadOnlySerializer, ElementCreateUpdateDestroySerializer, CategorySerializer, TypeSerializer, CommentSerializer, TodoSerializer

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
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Element.objects.all()
    serializer_class = ElementCreateUpdateDestroySerializer

class CategoryViewSet(viewsets.ModelViewSet):
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


# class TypeViewSet(viewsets.ReadOnlyModelViewSet):
class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    @action(detail=False, methods=['get'])
    def all(self, request):
         queryset = Type.objects.all()
         serializer = TypeSerializer(queryset, many=True)
         return Response(serializer.data)
    
    # def perform_create(self, serializer):
    #     print('Antes')
    #     print(self.request.data.get("title"))
    #     print(self.request.data.get("slug"))
       
    #     # type = Type()
    #     # type.title = self.request.data.get("title")
    #     # type.slug = self.request.data.get("slug")
    #     # type.save()
        
        
    #     type = Type.objects.create(
    #         title = self.request.data.get('title'),
    #         slug = self.request.data.get('slug')
    #     )
       
    #     # serializer.save()
    #     print("Despues")
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.exclude(element__isnull=True)
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
# Todo
class TodoViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Todo.objects.all().order_by('count')
    serializer_class = TodoSerializer
    
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by('count')
        # return super().get_queryset().filter(user=self.request.user).order_by('count')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, count=Todo.objects.filter(user=self.request.user).count()).save()
        
    @action(detail=False, methods=['post'])
    def sort(self, request):
        
        ids = request.POST.get('ids').split(',')

        for i, t in enumerate(ids):
            Todo.objects.filter(user=self.request.user).filter(id=t).update(count=i)
            
        return Response('OK')
    
    @action(detail=False, methods=['delete'])
    def delete(self, request):
        Todo.objects.filter(user=self.request.user).delete()
        return Response('OK')
        

    