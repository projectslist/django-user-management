from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from users.views import RegisterView,LoginView,UserView,ProfileUpdateView,DeleteUserView,UsersListView,AddUser,Predictor,LogoutView

class TestUrls(SimpleTestCase):

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_user_detail_url_resolves(self):
        url = reverse('user-detail')
        self.assertEqual(resolve(url).func.view_class, UserView)

    def test_profile_update_url_resolves(self):
        url = reverse('profile_update', args=['test@example.com'])
        self.assertEqual(resolve(url).func.view_class, ProfileUpdateView)

    def test_delete_user_url_resolves(self):
        url = reverse('delete_user', args=['test@example.com'])
        self.assertEqual(resolve(url).func.view_class, DeleteUserView)

    def test_users_list_url_resolves(self):
        url = reverse('users_list')
        self.assertEqual(resolve(url).func.view_class, UsersListView)

    def test_add_user_url_resolves(self):
        url = reverse('add_user')
        self.assertEqual(resolve(url).func.view_class, AddUser)

    def test_predictor_url_resolves(self):
        url = reverse('predictor')
        self.assertEqual(resolve(url).func.view_class, Predictor)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)
