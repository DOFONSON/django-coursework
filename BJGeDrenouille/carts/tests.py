from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from goods.models import Products, Companies
from carts.models import Cart

User = get_user_model()

class CartModelTest(TestCase):

    def setUp(self):
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
        self.cart = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=5
        )

    def test_cart_creation(self):
        self.assertEqual(str(self.cart), f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.cart.quantity}')
        self.assertEqual(self.cart.product, self.product)
        self.assertEqual(self.cart.quantity, 5)
        self.assertEqual(self.cart.products_price(), round(self.product.sell_price() * 5, 2))

class CartViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.company = Companies.objects.create(name='Test Company', slug='test-company')
        self.product = Products.objects.create(
            name='Test Product',
            slug='test-product',
            price=100.00,
            discount=10.00,
            quantity=50,
            company=self.company
        )

    def test_cart_add_authenticated_user(self):
        response = self.client.post(reverse('carts:cart_add'), {'product_id': self.product.id})
        self.assertEqual(response.status_code, 200)
        cart_item = Cart.objects.get(user=self.user, product=self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_cart_add_anonymous_user(self):
        self.client.logout()
        session = self.client.session
        session.create()
        session.save()
        response = self.client.post(reverse('carts:cart_add'), {'product_id': self.product.id})
        self.assertEqual(response.status_code, 200)
        cart_item = Cart.objects.get(session_key=session.session_key, product=self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_cart_change(self):
        cart_item = Cart.objects.create(user=self.user, product=self.product, quantity=1)
        response = self.client.post(reverse('carts:cart_change'), {'cart_id': cart_item.id, 'quantity': 3})
        self.assertEqual(response.status_code, 200)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)

    def test_cart_remove(self):
        cart_item = Cart.objects.create(user=self.user, product=self.product, quantity=1)
        response = self.client.post(reverse('carts:cart_remove'), {'cart_id': cart_item.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Cart.objects.filter(id=cart_item.id).exists())

