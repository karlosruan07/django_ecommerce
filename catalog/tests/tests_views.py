
from django.http import response
from django.test import TestCase, Client

class IndexViewTestCase(TestCase):
    
    def test_status_code(self):
        client = Client()
        response = client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_template_used(self):
        client = Client()
        response = client.get('/')
        self.assertTemplateUsed(response, 'catalog/lista_produtos.html')
    
    
    
    