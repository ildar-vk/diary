from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Entry

User = get_user_model()


class EntryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com', password='Test12345'
        )
        self.entry = Entry.objects.create(
            title='Тестовая запись',
            content='Содержание записи',
            author=self.user
        )

    def test_entry_creation(self):
        self.assertEqual(self.entry.title, 'Тестовая запись')
        self.assertEqual(self.entry.author.email, 'test@test.com')

    def test_entry_str(self):
        self.assertEqual(str(self.entry), 'Тестовая запись')

    def test_entry_ordering(self):
        entry2 = Entry.objects.create(
            title='Старая запись', content='...', author=self.user
        )
        entries = Entry.objects.all()
        self.assertEqual(entries[0], entry2)
        self.assertEqual(entries[1], self.entry)


class EntryViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com', password='Test12345'
        )
        self.other_user = User.objects.create_user(
            email='other@test.com', password='Test12345'
        )
        self.client.login(username='test@test.com', password='Test12345')
        self.entry = Entry.objects.create(
            title='Моя запись', content='Моё содержание', author=self.user
        )
        self.other_entry = Entry.objects.create(
            title='Чужая запись', content='Чужое содержание', author=self.other_user
        )

    def test_entry_list_view(self):
        response = self.client.get(reverse('entry_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Моя запись')
        self.assertNotContains(response, 'Чужая запись')

    def test_entry_detail_view(self):
        response = self.client.get(reverse('entry_detail', args=[self.entry.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Моё содержание')

    def test_entry_detail_other_user_denied(self):
        response = self.client.get(reverse('entry_detail', args=[self.other_entry.pk]))
        self.assertEqual(response.status_code, 404)

    def test_entry_create_view(self):
        response = self.client.post(reverse('entry_create'), {
            'title': 'Новая запись', 'content': 'Новое содержание'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.filter(author=self.user).count(), 2)

    def test_entry_update_view(self):
        response = self.client.post(
            reverse('entry_update', args=[self.entry.pk]),
            {'title': 'Обновлено', 'content': 'Обновлённое содержание'}
        )
        self.assertEqual(response.status_code, 302)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, 'Обновлено')

    def test_entry_update_other_user_denied(self):
        response = self.client.post(
            reverse('entry_update', args=[self.other_entry.pk]),
            {'title': 'Взлом', 'content': '...'}
        )
        self.assertEqual(response.status_code, 404)

    def test_entry_delete_view(self):
        response = self.client.post(reverse('entry_delete', args=[self.entry.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.filter(author=self.user).count(), 0)

    def test_entry_delete_other_user_denied(self):
        response = self.client.post(reverse('entry_delete', args=[self.other_entry.pk]))
        self.assertEqual(response.status_code, 404)

    def test_search(self):
        response = self.client.get(reverse('entry_list') + '?q=Моя')
        self.assertContains(response, 'Моя запись')
        self.assertNotContains(response, 'Чужая запись')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('entry_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class AuthTest(TestCase):
    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'email': 'new@test.com', 'password': 'NewUser12345'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='new@test.com').exists())

    def test_login_view(self):
        User.objects.create_user(email='login@test.com', password='Test12345')
        response = self.client.post(reverse('login'), {
            'username': 'login@test.com',
            'password': 'Test12345'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
