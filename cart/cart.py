from decimal import Decimal

from my_shop import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        """initializes the cart attributes"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """adds a new product to the cart or overrides the quantity"""
        product_id = product.id
        if not product_id in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        """removes a product from the shopping cart"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
            a method to auto-assign price and total values to every product in the cart
            it also enables us to use for loop on cart object in views and templates loops
        :return:
        """

        products = Product.objects.filter(id__in=self.cart.keys())
        cart = self.cart.copy()

        # assigning product objects to each product in cart
        for product in products:
            cart[str(product.id)]['product'] = product

        # assigning total and price values
        for product in cart.values():
            product['total'] = Decimal(product['price']) * Decimal(product['quantity'])
            yield product

    def __len__(self):
        """
            :returns the totoal amount of things in the cart
        """
        return sum([item['quantity'] for item in self.cart.values()])

    def get_total_price(self):
        """
        :returns the total cost of all items in the cart
        """
        return sum([Decimal(item['price']) * item['quantity'] for item in self.cart.values()])

    def clear(self):
        """
            removes cart form the session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()  # warn that the session was modified
