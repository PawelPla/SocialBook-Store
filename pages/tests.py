from django.test import SimpleTestCase
from django.urls import reverse, resolve

from pages.views import AboutPageView


class PagesTests(SimpleTestCase):
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Homepage')
        self.assertNotContains(response, 'Invalid text')

    def test_about_page(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')
        self.assertNotContains(response, 'Invalid text')

    def test_name_spaces(self):
        response_home = self.client.get(reverse('home'))
        self.assertEqual(response_home.status_code, 200)
        response_home = self.client.get(reverse('about'))
        self.assertEqual(response_home.status_code, 200)

    def test_aboutpage_url_resolves_aboutpageview(self):
        view = resolve('/about/')
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)
        self.assertEqual(view.view_name, 'about')
