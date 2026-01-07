from django.test import TestCase, Client
from rest_framework.test import APITestCase, APIClient

from comments.forms import CommentForm
from comments.models import Comment
from elements.models import Element, Category, Type
from api.serializers import CommentSerializer


# Create your tests here.

class CommentTest(TestCase):
    def setUp(self):

        Comment.objects.create(text='text 1')
        Comment.objects.create(text='text 2')

        self.comments = Comment.objects.all()
        self.client = Client()
        return super().setUp()
    
    def test_index(self):

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,self.comments[0].text)
        self.assertContains(response,self.comments[1].text)
        self.assertTemplateUsed(response, "comments/index.html")

    def test_post_get(self):
        response = self.client.get("/add")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'<textarea name="text"')
        # self.assertHTMLEqual(response.content.decode(),'<textarea name="text"')
        # self.assertInHTML(response.content.decode(),'<textarea name="text"')
        self.assertTemplateUsed(response, "comments/add.html")

    def test_post_post(self):
        text = 'text comment'
        response = self.client.post("/add" , {'text':text})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        comment = Comment.objects.order_by('-id')[0]

        self.assertEqual(comment.text,text)

    def test_update_get(self):

        comment = Comment.objects.get(id=2)
        response = self.client.get("/update/"+str(comment.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,f'<textarea name="text" cols="40" rows="10" required id="id_text">\n{comment.text}')
        self.assertTemplateUsed(response, "comments/add.html")
        
    def test_update_post(self):
        comment = Comment.objects.get(id=2)
        text = 'text comment new'
        response = self.client.post("/update/"+str(comment.id) , {'text':text})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
    
        comment_updated = Comment.objects.get(id=2)
        self.assertEqual(comment_updated.text,text)
        
    def test_delete_post(self):
        comment = Comment.objects.get(id=2)
        response = self.client.post("/delete/"+str(comment.id))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
    
        try:
            Comment.objects.get(id=2)
            raise Exception('El comentario deberia haber sido eliminado')
        except Comment.DoesNotExist:
            pass
    
class CommentFormTest(TestCase):
    def test_comment_fields(self):
        form = CommentForm()
        self.assertTrue(form.fields['text'] is not None)
        self.assertTrue(form.fields['text'].label is not None)

    def test_comment_valid(self):
        form = CommentForm(data={'text':'Comment'})
        self.assertTrue(form.is_valid())

    def test_comment_invalid(self):
        form = CommentForm(data={'text':''})
        self.assertFalse(form.is_valid())

    def test_comment_create(self):
        form = CommentForm(data={'text':'Comment'})
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertTrue(comment.id==1)

    def test_comment_update(self):
        comment = Comment.objects.create(text='text')
        text='new text'
        form = CommentForm(data={'text':text}, instance=comment)
        # print(form.data['text'])
        self.assertTrue(form.is_valid())
        comment = form.save()
        # comment = Comment.objects.get(id=comment.id)
        self.assertTrue(comment.text==text)

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