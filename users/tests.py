from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase
from django.urls import reverse
import os
from books.models import Book, Review
from users.forms import UpdateUserForm

User = get_user_model()


class CustomUserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@user.com',
            password='testing321',
            age=18,
            profile_pic=File(open('static/images/gandalf.jpg', 'rb'))
        )
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='super@user.com',
            password='testing321',
            age=18,
        )

    def test_custom_user_create(self):
        user = self.user
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@user.com')
        self.assertEqual(user.age, 18)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_custom_super_user_create(self):
        user = self.superuser
        self.assertEqual(user.username, 'superuser')
        self.assertEqual(user.email, 'super@user.com')
        self.assertEqual(user.age, 18)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_custom_user_with_incomplete_data(self):
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(username='')
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', password="foo")

    def test_custom_user_superuser_with_incomplete_data(self):
        with self.assertRaises(TypeError):
            User.objects.create_superuser()
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username='')
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username='', password="foo")
        with self.assertRaises(TypeError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)

    def test_custom_user_num_reviews_before_any_added(self):
        self.assertEqual(self.user.num_reviews(), 0)


class SignupTests(TestCase):
    username = 'newuser'
    email = 'newuser@email.com'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertTemplateUsed(self.response, '_base.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'Something that should not be there.')

    def test_signup_form(self):
        queryset = get_user_model().objects.all()
        new_user = get_user_model().objects.create_user(
            self.username, self.email
        )
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0].username, self.username)
        self.assertEqual(queryset[0].email, self.email)
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class UserDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@user.com',
            password='testing321',
            age=18,
        )

    def test_user_detail_not_logged_in(self):
        url = reverse('profile_detail', kwargs={'pk': str(self.user.pk)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')

    def test_user_detail_logged_in(self):
        self.client.login(email='test@user.com', password='testing321')
        url = reverse('profile_detail', kwargs={'pk': str(self.user.pk)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 404)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.first_name)
        self.assertNotContains(response, 'Text not included')
        self.assertTemplateUsed(response, 'profile/profile_detail.html')
        self.assertTemplateUsed(response, '_base.html')


class AllUsersTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test2@user.com',
            password='testing321',
            age=18,
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test1@user.com',
            password='testing321',
            age=18,
        )
        self.url = reverse('all_users')

    def test_all_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Unwanted text')
        self.assertTemplateUsed(response, 'profile/profile_list.html')
        self.assertTemplateUsed(response, '_base.html')
        self.assertContains(response, 'All users')
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user1.age)
        self.assertContains(response, self.user2.username)
        self.assertContains(response, self.user2.age)
        self.assertNotContains(response, 'Text not included')
        self.assertNotContains(response, self.user1.password)

    def test_all_users_logged_in_and_not(self):
        self.client.login(email=self.user1.email, password='testing321')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        self.client.logout()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 302)


class TopReviewersTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser1',
            email='test2@user.com',
            password='testing321',
            age=18,
        )
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
        self.response = self.client.get(reverse('top_reviewers'))

    def test_top_reviewers(self):
        resp = self.response
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.status_code, 404)
        self.assertContains(resp, self.user)
        self.assertContains(resp, self.user.num_reviews())
        self.assertTemplateUsed(resp, 'profile/top_reviewers.html')
        self.assertTemplateUsed(resp, '_base.html')

    def test_top_users_logged_in_and_not(self):
        resp = self.response
        self.client.login(email=self.user.email, password='testing321')
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.status_code, 404)
        self.client.logout()
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.status_code, 302)


class UpdateUserFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@user.com',
            password='testing321',
            age=18,
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@user.com',
            password='testing321',
            age=19,
        )
        self.url = reverse('profile_update', kwargs={'pk': str(self.user.pk)})

    def test_from_with_valid_data(self):
        form = UpdateUserForm(data={
            'first_name': 'Test',
            'last_name': 'Smith',
            'profile_pic': File(open('static/images/gandalf.jpg', 'rb'))
        })
        self.assertTrue(form.is_valid())
        updated = form.save(commit=True)
        self.assertEqual(updated.first_name, "Test")
        self.assertEqual(updated.last_name, "Smith")

    def test_form_with_blank_data(self):
        form = UpdateUserForm({})
        self.assertTrue(form.is_valid())

    def test_user_update_not_logged(self):
        resp = self.client.get(self.url)
        self.assertNotContains(resp, 'First Name', 302)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'{reverse("account_login")}?next={self.url}')

    def test_user_update_logged_in(self):
        self.client.login(email='test@user.com', password='testing321')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'First name')
        self.assertContains(resp, 'First name')
        self.assertTemplateUsed(resp, 'profile/profile_update.html')


class UserReviewsTests(TestCase):
    pass
