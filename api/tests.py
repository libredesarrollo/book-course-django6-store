from rest_framework.test import APITestCase, APIClient

from comments.models import Comment
from elements.models import Element, Category, Type
from api.serializers import CommentSerializer, ElementReadOnlySerializer

# Create your tests here.

class CommentApiTest(APITestCase):
    def setUp(self):
        category = Category()        
        category.title = 'Category 1'
        category.slug = 'category-1'
        category.save()
        
        type = Type()        
        type.title = 'type 1'
        type.slug = 'type-1'
        type.save()
        
        element = Element()        
        element.title = 'Element 1'
        element.slug = 'element-1'
        element.description = 'Description 1'
        element.category = category
        element.type = type
        element.save()

        self.comment = Comment.objects.create(text='Text 1', element=element)
        Comment.objects.create(text='Text 2', element=element)
        Comment.objects.create(text='Text 3', element=element)
        self.client = APIClient()
        
    def test_get_comments_pagination(self):
        response = self.client.get('/api/comment/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Text 1')
        self.assertContains(response, 'Text 2')
        self.assertContains(response, 'Text 3')
        
    def test_get_comments_detail(self):
            response = self.client.get('/api/comment/'+str(self.comment.id)+'/')
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.comment.text)
            
    def test_get_comments_detail_serializacion(self):
            response = self.client.get('/api/comment/'+str(self.comment.id)+'/')
            self.assertEqual(response.status_code, 200)
            # print(CommentSerializer(self.comment).data)
            self.assertJSONEqual(response.content, CommentSerializer(self.comment).data)
    def test_get_comments_create_success(self):
        data = { 'text':'Text 4' }
        response = self.client.post('/api/comment/', data)
        self.assertEqual(response.status_code, 201)
        # print(response)
        # print(response.content)
        bytes_dict_res = response.content
        dict_str = bytes_dict_res.decode('UTF-8').replace('null','""')
        # print(dict_str)
        # data_dict = ast.literal_eval(dict_str)
        data_dict = eval(dict_str)
        # print(data_dict)
        # print(data_dict.get('id'))
        self.comment = comment = Comment.objects.get(id=data_dict.get('id'))
        self.assertEqual(comment.text, data.get('text'))
        
        # self.test_get_comments_detail_serializacion()
        # response = self.client.get('/api/comment/'+str(data_dict.get('id'))+'/')
        # self.assertEqual(response.status_code, 200)
        
    def test_update_success(self):
        data = { 'text':'New Text' }
        
        response = self.client.put('/api/comment/'+str(self.comment.id)+'/', data)
        self.assertEqual(response.status_code, 200)
     
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.text, data.get('text'))

        # Verificar en BD O REST API        
        # response = self.client.get('/api/comment/'+str(self.comment.id)+'/')
        # self.assertEqual(response.status_code, 200)
        # self.assertContains(response, data.get('text'))

    def test_delete(self):
        response = self.client.delete('/api/comment/'+str(self.comment.id)+'/')
        self.assertEqual(response.status_code, 204)

        try:
            Comment.objects.get(pk=self.comment.id)
            raise Exception('El comentario deberia haber sido eliminado')
        except Comment.DoesNotExist:
            pass
    
    def test_comment_serializer(self):
        cs = CommentSerializer(self.comment).data
        self.assertEqual(cs['id'], self.comment.id)
        self.assertEqual(cs['text'], self.comment.text)
        self.assertEqual(cs['count'], Comment.objects.filter(element_id = self.comment.element_id).count())
     
    def test_create_error_form(self):
        data = {'text':''}
        response = self.client.post('/api/comment/',data)
        self.assertEqual(response.status_code,400)
        self.assertJSONEqual(response.content, '{ "text": [ "This field may not be blank." ] }')
    def test_create_error_form_empty(self):
        data = {}
        response = self.client.post('/api/comment/',data)
        self.assertEqual(response.status_code,400)
        self.assertJSONEqual(response.content, '{ "text": [ "This field is required." ] }')

class ElementApiTest(APITestCase):
    def setUp(self):
        self.category = Category()        
        self.category.title = 'Category 1'
        self.category.slug = 'category-1'
        self.category.save()
        
        self.type = Type()        
        self.type.title = 'type 1'
        self.type.slug = 'type-1'
        self.type.save()
        
        self.element = Element()        
        self.element.title = 'Element 1'
        self.element.slug = 'element-1'
        self.element.description = 'Description 1'
        self.element.category = self.category
        self.element.type = self.type
        self.element.save()

        self.client = APIClient()
        
    def test_get_elements_pagination(self):
        response = self.client.get('/api/element-lecture/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Element 1')
        
    def test_get_elements_detail(self):
        response = self.client.get('/api/element-lecture/'+str(self.element.id)+'/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.element.title)
            
    def test_get_elements_detail_serialization(self):
        response = self.client.get('/api/element-lecture/'+str(self.element.id)+'/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, ElementReadOnlySerializer(self.element).data)

    def test_create_element_success(self):
        data = {
            'title': 'Element 2',
            'slug': 'element-2',
            'description': 'Description 2',
            'price': 20.00,
            'category': self.category.id,
            'type': self.type.id
        }
        response = self.client.post('/api/element-write/', data)
        self.assertEqual(response.status_code, 201)
        
        element = Element.objects.get(slug='element-2')
        self.assertEqual(element.title, data.get('title'))
        
    def test_update_element_success(self):
        data = {
            'title': 'Element Updated',
            'slug': 'element-1',
            'description': 'Description Updated',
            'price': 15.00,
            'category': self.category.id,
            'type': self.type.id
        }
        
        response = self.client.put('/api/element-write/'+str(self.element.id)+'/', data)
        self.assertEqual(response.status_code, 200)
     
        element = Element.objects.get(id=self.element.id)
        self.assertEqual(element.title, data.get('title'))

    def test_delete_element(self):
        response = self.client.delete('/api/element-write/'+str(self.element.id)+'/')
        self.assertEqual(response.status_code, 204)

        try:
            Element.objects.get(pk=self.element.id)
            raise Exception('El elemento deberia haber sido eliminado')
        except Element.DoesNotExist:
            pass