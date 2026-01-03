from django.test import TestCase, Client

from .models import Comment


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
    
        

