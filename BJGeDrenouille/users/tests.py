from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.core.files.uploadedfile import SimpleUploadedFile

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm

User = get_user_model()

class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_creation(self):
        self.assertEqual(str(self.user), 'testuser')
        self.assertTrue(self.user.check_password('testpass'))

class UserViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.company = Companies.objects.create(name='Test Company', slug='test-company')
        self.product = Products.objects.create(
            name='Test Product',
            slug='test-product',
            price=100.00,
            discount=10.00,
            quantity=50,
            company=self.company
        )
        self.cart_item = Cart.objects.create(user=self.user, product=self.product, quantity=5)

    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], UserLoginForm)

        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(auth.get_user(self.client).is_authenticated)

    def test_registration_view(self):
        response = self.client.get(reverse('users:registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertIsInstance(response.context['form'], UserRegistrationForm)

        response = self.client.post(reverse('users:registration'), {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username='newuser')
        self.assertTrue(new_user.is_authenticated)

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIsInstance(response.context['form'], ProfileForm)

        avatar = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        response = self.client.post(reverse('users:profile'), {
            'username': 'updateduser',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'image': avatar
        })
        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.first_name, 'Test')
        self.assertEqual(updated_user.last_name, 'User')
        self.assertEqual(updated_user.phone_number, '1234567890')

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_users_cart_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('users:users_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/users_cart.html')

