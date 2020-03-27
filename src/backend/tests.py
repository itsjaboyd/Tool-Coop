from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import Order, OrderItem, ToolType,Tool
from django.test.utils import setup_test_environment
from django.urls import reverse
# Create your tests here.
class ToolOrderTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        # self.factory = RequestFactory()
        print("--------------------------------------------------------------\n\n")
        client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@gmail.com', password='top_secret')
        self.client.login(username='testuser', password='top_secret')
        ToolType.objects.create(type_name='Axe', description='this is a test.', slug='axe')
        tool = ToolType.objects.get(slug='axe')
        for x in range(5):
            Tool.objects.create(tool_type=tool, is_available=True)

    def test_tool_create(self):
        print("Begin Tool Create Test")
        print("Test new tools create")
        ToolType.objects.create(type_name='Hammer', description='this is a test.', slug='hammer')
        tool = ToolType.objects.get(slug='hammer')
        self.assertEqual(tool.type_name, "Hammer")
        print("Tool Create Test Passed!\n\n")

    def test_remove_from_cart(self):
        print("Begin Remove Tool Test")
        tool = ToolType.objects.get(slug='axe')
        self.client.get(tool.get_add_to_cart_url())
        print("Testing return URl: ")
        response = self.client.get(tool.get_remove_tool_from_cart())
        self.assertEqual(response.url, "/order-summary/")
        print("Testing order found: ")
        self.assertEqual( Order.objects.filter(user=self.user, is_reserved=False).exists(), True)
        order = Order.objects.get(user=self.user, is_reserved=False)
        print("Testing order item removed from order: ")
        for item in order.items.all():
            print(item)
        self.assertEqual(order.items.filter(tool_id=tool.id).exists(), False)
        print("Remove Tool Test Passed!\n\n")

    def test_remove_single_tool_from_cart(self):
        print("Begin Remove Single Tool Test")
        #setup for test case
        tool = ToolType.objects.get(slug='axe')
        self.client.get(tool.get_add_to_cart_url())
        self.client.get(tool.get_add_to_cart_url())
        order = Order.objects.get(user=self.user, is_reserved=False)
        order_item= order.items.get(tool_id=tool.id)
        print("Axes in cart: "+ str(order_item.quantity))
        print("Testing return URl: ")
        response = self.client.get(tool.get_remove_single_from_cart_url())
        self.assertEqual(response.url, "/order-summary/")
        
        print("Testing order found: ")
        self.assertEqual( Order.objects.filter(user=self.user, is_reserved=False).exists(), True)
        order = Order.objects.get(user=self.user, is_reserved=False)
        print("Testing 1 item removed: ")
        order_item= order.items.get(tool_id=tool.id)
        self.assertEqual(order_item.quantity, 1)
        print("Axes in cart: "+ str(order_item.quantity))
        print("Remove Single Tool Test Passed!\n\n")

    def test_add_to_cart(self):
        print("Begin Tool Add To Cart Test")
        tool = ToolType.objects.get(slug='axe')
        print("Testing return URl: ")
        response = self.client.get(tool.get_add_to_cart_url())
        self.assertEqual(response.url, "/order-summary/")
        print("Testing order created: ")
        self.assertEqual( Order.objects.filter(user=self.user, is_reserved=False).exists(), True)
        order = Order.objects.get(user=self.user, is_reserved=False)
        print("Testing order item created: ")
        self.assertEqual( order.items.filter(tool_id=tool.id).exists(), True)
        print("Testing order item quanitity updated: ")
        order_item= order.items.get(tool_id=tool.id)
        print("Testing additional tool added to cart: ")
        self.client.get(tool.get_add_to_cart_url())
        order_item= order.items.get(tool_id=tool.id)
        self.assertEqual(order_item.quantity, 2)
        
        print("Tool Add To Cart Test Passed!")

    


    # def test_order_model():
    #     pass
    
    # def test_order_item_model():
    #     pass

    # def test_order_model():
    #     pass