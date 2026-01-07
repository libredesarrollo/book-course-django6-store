from django.test import TestCase

from elements.forms import ElementForm
from elements.models import Element, Category, Type

class ElementFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category 1', slug='category-1')
        self.type = Type.objects.create(title='Type 1', slug='type-1')

    def test_element_fields(self):
        form = ElementForm()
        self.assertTrue(form.fields['title'] is not None)
        self.assertTrue(form.fields['description'] is not None)
        self.assertTrue(form.fields['price'] is not None)
        self.assertTrue(form.fields['category'] is not None)
        self.assertTrue(form.fields['type'] is not None)

    def test_element_valid(self):
        data = {
            'title': 'Element Test',
            'slug': 'element-test',
            'description': 'Description Test',
            'price': 10.00,
            'category': self.category.id,
            'type': self.type.id
        }
        form = ElementForm(data=data)
        self.assertTrue(form.is_valid())

    def test_element_invalid(self):
        data = {
            'title': '',
            'description': 'Description Test',
            'price': 10.00,
            'category': self.category.id,
            'type': self.type.id
        }
        form = ElementForm(data=data)
        self.assertFalse(form.is_valid())

    def test_element_create(self):
        data = {
            'title': 'Element Create',
            'slug': 'element-create',
            'description': 'Description Create',
            'price': 20.00,
            'category': self.category.id,
            'type': self.type.id
        }
        form = ElementForm(data=data)
        self.assertTrue(form.is_valid())
        element = Element.objects.create(
            title=form.cleaned_data['title'],
            slug=form.cleaned_data['slug'],
            description=form.cleaned_data['description'],
            price=form.cleaned_data['price'],
            category=form.cleaned_data['category'],
            type=form.cleaned_data['type']
        )
        self.assertTrue(element.id is not None)

    def test_element_update(self):
        element = Element.objects.create(title='Element Original', slug='element-original', description='Desc Original', price=10.00, category=self.category, type=self.type)
        title = 'Element Updated'
        form = ElementForm(data={'title': title, 'slug': 'element-original', 'description': 'Desc Original', 'price': 10.00, 'category': self.category.id, 'type': self.type.id})
        self.assertTrue(form.is_valid())
        element.title = form.cleaned_data['title']
        element.slug = form.cleaned_data['slug']
        element.description = form.cleaned_data['description']
        element.price = form.cleaned_data['price']
        element.category = form.cleaned_data['category']
        element.type = form.cleaned_data['type']
        element.save()
        self.assertTrue(element.title == title)