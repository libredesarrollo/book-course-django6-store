from django.test import TestCase

from comments.forms import CommentForm
from comments.models import Comment

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
