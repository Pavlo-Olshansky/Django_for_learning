from django.test import TestCase
from .models import *
import unittest
from django.test import Client

class PostBlogTests(TestCase):
    def test_recent_pub(self):
        future_data = timezone.now().date() + datetime.timedelta(days=5)
        future_blog = Post_blog(time=future_data)
        self.assertEqual(future_blog.recent_publication(), False)

class UnitPageTest(unittest.TestCase):
    def test_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_blog(self):
        client = Client()
        response = client.get('/blog/')
        self.assertEqual(response.status_code, 200)

class PageTest(TestCase):
    def test_contact(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
