from django.test import TestCase, Client

from .models import Comment


# Create your tests here.

class CommentTest(TestCase):
    def setUp(self):

        Comment.objects.create(text='text 1')
        Comment.objects.create(text='text 2')

        self.client = Client()
        return super().setUp()
    
    def test_index(self):
        response = self.client.get("/")

        Comment.objects.create(text='text 2')
        assert response.status_code == 200
        

