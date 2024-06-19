from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from goods.models import Products, Companies
from carts.models import Cart
from orders.models import Order, OrderItem
from orders.forms import CreateOrderForm

User = get_user_model()

class OrderModelTest(TestCase):

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
        self.order = Order.objects.create(
            user=self.user,
            phone_number='1234567890',
            requires_delivery=True,
            delivery_address='Test Address',
            payment_on_get=False
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            name=self.product.name,
            price=self.product.sell_price(),
            quantity=10
        )

    def test_order_creation(self):
        self.assertEqual(str(self.order), f"Заказ № {self.order.pk} | Покупатель {self.user.first_name} {self.user.last_name}")
        self.assertEqual(self.order.phone_number, '1234567890')
        self.assertEqual(self.order.requires_delivery, True)
        self.assertEqual(self.order.delivery_address, 'Test Address')
        self.assertEqual(self.order.payment_on_get, False)
        self.assertEqual(self.order.status, 'В обработке')

    def test_order_item_creation(self):
        self.assertEqual(str(self.order_item), f"Товар {self.order_item.name} | Заказ № {self.order.pk}")
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.price, self.product.sell_price())
        self.assertEqual(self.order_item.quantity, 10)
        self.assertEqual(self.order_item.products_price(), round(self.product.sell_price() * 10, 2))

class CreateOrderViewTest(TestCase):

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
        self.cart_item = Cart.objects.create(user=self.user, product=self.product, quantity=5)

    def test_create_order_get(self):
        response = self.client.get(reverse('orders:create_order'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/create_order.html')
        self.assertIsInstance(response.context['form'], CreateOrderForm)

    def test_create_order_post(self):
        form_data = {
            'phone_number': '1234567890',
            'requires_delivery': True,
            'delivery_address': 'Test Address',
            'payment_on_get': False
        }
        response = self.client.post(reverse('orders:create_order'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user:profile'))

        order = Order.objects.get(user=self.user)
        self.assertEqual(order.phone_number, '1234567890')
        self.assertEqual(order.requires_delivery, True)
        self.assertEqual(order.delivery_address, 'Test Address')
        self.assertEqual(order.payment_on_get, False)

        order_item = OrderItem.objects.get(order=order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 5)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Заказ оформлен!')

    def test_create_order_insufficient_stock(self):
        self.product.quantity = 4
        self.product.save()
        form_data = {
            'phone_number': '1234567890',
            'requires_delivery': True,
            'delivery_address': 'Test Address',
            'payment_on_get': False
        }
        response = self.client.post(reverse('orders:create_order'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:order'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Недостаточное количество товара', str(messages[0]))

        self.assertFalse(Order.objects.filter(user=self.user).exists())
