from django.test import TestCase, Client

from elements.models import Element, Category, Type

class ElementTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category 1', slug='category-1')
        self.type = Type.objects.create(title='Type 1', slug='type-1')

        Element.objects.create(title='Element 1', slug='element-1', description='Desc 1', category=self.category, type=self.type)
        Element.objects.create(title='Element 2', slug='element-2', description='Desc 2', category=self.category, type=self.type)

        self.elements = Element.objects.all()
        self.client = Client()
        return super().setUp()
    
    def test_index(self):
        response = self.client.get("/elements/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.elements[0].title)
        self.assertContains(response, self.elements[1].title)
        self.assertTemplateUsed(response, "elements/index.html")

    def test_post_get(self):
        response = self.client.get("/elements/add")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input type="text" name="title"')
        self.assertTemplateUsed(response, "elements/add.html")

    def test_post_post(self):
        title = 'Element 3'
        data = {
            'title': title,
            'slug': 'element-3',
            'description': 'Desc 3',
            'price': 30.00,
            'category': self.category.id,
            'type': self.type.id
        }
        response = self.client.post("/elements/add", data)
        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, '/elements/')
        
        element = Element.objects.get(slug='element-3')
        self.assertEqual(element.title, title)

    def test_update_get(self):
        element = self.elements[0]
        response = self.client.get("/elements/update/"+str(element.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, element.title)
        self.assertTemplateUsed(response, "elements/add.html")
        
    def test_update_post(self):
        element = self.elements[0]
        title = 'Element Updated'
        data = {
            'title': title,
            'slug': element.slug,
            'description': element.description,
            'price': element.price,
            'category': self.category.id,
            'type': self.type.id
        }
        response = self.client.post("/elements/update/"+str(element.id), data)
        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, '/elements/')
    
        element_updated = Element.objects.get(id=element.id)
        self.assertEqual(element_updated.title, title)
        
    def test_delete_post(self):
        element = self.elements[1]
        response = self.client.post("/elements/delete/"+str(element.id))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/elements/')
    
        try:
            Element.objects.get(id=element.id)
            raise Exception('El elemento deberia haber sido eliminado')
        except Element.DoesNotExist:
            pass