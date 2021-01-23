from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from books.models import Book, Review


class BookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='reviewuser',
            email='reviewuser@email.com',
            password='testpass123'
        )
        self.special_permission = Permission.objects.get(codename='all_books_status')
        self.book = Book.objects.create(
            title='Some test title',
            author='Some test author',
            price='39.11'
        )
        self.review = Review.objects.create(
            book=self.book,
            content='Test content',
            author=self.user
        )

    def test_book_listing(self):
        self.assertEqual(self.book.title, 'Some test title')
        self.assertEqual(self.book.author, 'Some test author')
        self.assertEqual(self.book.price, '39.11')

    def test_user_model(self):
        self.assertEqual(self.user.username, 'reviewuser')
        self.assertEqual(self.user.email, 'reviewuser@email.com')

    def test_review_model(self):
        self.assertEqual(self.review.book, self.book)
        self.assertEqual(self.review.content, 'Test content')
        self.assertEqual(self.review.author.username, 'reviewuser')

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(email='reviewuser@email.com', password='testpass123')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, 'Some test title')
        self.assertContains(response, 'Some test author')
        self.assertNotContains(response, 'Unwanted text')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next=/books/')
        response = self.client.get(f'{reverse("account_login")}?next=/books/')
        self.assertContains(response, 'Log In')

    def test_get_absolute_url_works_correctly(self):
        response_get_absolute_url = self.client.get(self.book.get_absolute_url())
        response_url_with_pk = self.client.get(f'/books/{self.book.pk}/')
        self.assertEqual(response_get_absolute_url.status_code, response_url_with_pk.status_code)

    def test_book_detail_view_with_permissions(self):
        self.client.login(email='reviewuser@email.com', password='testpass123')
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Some test title')
        self.assertContains(response, 'Some test author')
        self.assertContains(response, '39.11')
        self.assertContains(response, 'Test content')
        self.assertTemplateUsed(response, 'books/book_detail.html')

    def test_book_detail_view_no_permissions(self):
        self.client.login(email='reviewuser@email.com', password='testpass123')
        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 403)