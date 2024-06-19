from django.test import TestCase, Client
from django.urls import reverse
from goods.models import Companies, Products

class CompaniesModelTest(TestCase):
    
    def setUp(self):
        self.company = Companies.objects.create(
            name="Test Company",
            slug="test-company"
        )

    def test_company_creation(self):
        self.assertEqual(self.company.name, "Test Company")
        self.assertEqual(self.company.slug, "test-company")
        self.assertEqual(str(self.company), "Test Company")

class ProductsModelTest(TestCase):
    
    def setUp(self):
        self.company = Companies.objects.create(
            name="Test Company",
            slug="test-company"
        )
        self.product = Products.objects.create(
            name="Test Product",
            slug="test-product",
            price=100.00,
            discount=10.00,
            quantity=50,
            company=self.company
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.slug, "test-product")
        self.assertEqual(self.product.price, 100.00)
        self.assertEqual(self.product.discount, 10.00)
        self.assertEqual(self.product.quantity, 50)
        self.assertEqual(self.product.company, self.company)
        self.assertEqual(str(self.product), "Test Product Колличество - 50")

    def test_sell_price(self):
        self.assertEqual(self.product.sell_price(), 90.00)

    def test_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), "/catalog/product/test-product/")

class CatalogViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Companies.objects.create(
            name="Test Company",
            slug="test-company"
        )
        self.product1 = Products.objects.create(
            name="Test Product 1",
            slug="test-product-1",
            price=100.00,
            discount=10.00,
            quantity=50,
            company=self.company
        )
        self.product2 = Products.objects.create(
            name="Test Product 2",
            slug="test-product-2",
            price=200.00,
            discount=0.00,
            quantity=30,
            company=self.company
        )

    def test_catalog_view(self):
        response = self.client.get(reverse('catalog:catalog', kwargs={'company_slug': 'test-company'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/catalog.html')
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_catalog_view_with_query(self):
        response = self.client.get(reverse('catalog:catalog', kwargs={'company_slug': 'all'}), {'q': 'Test Product 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_catalog_view_on_sale(self):
        response = self.client.get(reverse('catalog:catalog', kwargs={'company_slug': 'test-company'}), {'on_sale': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)

    def test_catalog_view_pagination(self):
        response = self.client.get(reverse('catalog:catalog', kwargs={'company_slug': 'test-company'}), {'page': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/catalog.html')
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

class ProductViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Companies.objects.create(
            name="Test Company",
            slug="test-company"
        )
        self.product = Products.objects.create(
            name="Test Product",
            slug="test-product",
            price=100.00,
            discount=10.00,
            quantity=50,
            company=self.company
        )

    def test_product_view(self):
        response = self.client.get(reverse('catalog:product', kwargs={'product_slug': 'test-product'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/product.html')
        self.assertContains(response, self.product.name)
