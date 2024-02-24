from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Post


# Create your tests here.
class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )
        self.post = Post.objects.create(
            title='A good title',
            body='Nice body content',
            author=self.user
        )

    def test_string_representation(
            self):  # Compara si el titulo que le colocamos al post es igual al que convierte a str
        post = Post(title='A simple title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):  # Comparamos el contenido de cada elemento del post creado con lo que deberia de tener
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.body}', 'Nice body content')
        self.assertEqual(f'{self.post.author}', 'testuser')

    def test_post_list_view(
            self):  # Comparamos que la respuesta sea 200, que contenga el titulo y se use el template home
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail(self):  # Comparamos que la respuesta sea 200 para el pk 1 y 404 para el que no existe
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_create_view(self):  # Test del form
        response = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'body': 'New text',
            'author': self.user.id
        })
        self.assertEqual(response.status_code, 302)  # Se pone el 302 porque te esta redireccionado
        self.assertEqual(Post.objects.last().title, 'New title')
        self.assertEqual(Post.objects.last().body, 'New text')

    def test_post_update_view(self): #Actualizar
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated Title',
            'body': 'Updated text'
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):#Eliminar
        response = self.client.post(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)
