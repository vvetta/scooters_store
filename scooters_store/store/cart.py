from decimal import Decimal
from django.conf import settings
from .models import Product

"""В этом файле находиться класс пользовательской корзины, которая храниться в сессии."""


class Cart(object):

    def __init__(self, request):
        """Инициализируем корзину."""

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {'products': []}
        self.cart = cart

    def add(self, product):
        """Добавить продукт в корзину."""

        product_id = str(product.slug)

        if product_id not in [item['slug'] for item in self.cart['products']]:
            self.cart['products'].append({'price': str(product.price),
                                          'title': product.title,
                                          'description': product.description,
                                          'slug': product.slug,
                                          'photo': str(product.photo),
                                          'quantity': 1})
        else:
            for item in self.cart['products']:
                if item['slug'] == product_id:
                    item['quantity'] += 1

        self.save()

    def save(self):

        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart

        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины."""

        product_id = str(product.slug)
        for product in self.cart['products']:
            if product['slug'] == product_id and product['quantity'] == 1:
                self.cart['products'].remove(product)
                self.save()
            elif product['slug'] == product_id and product['quantity'] > 1:
                product['quantity'] = product['quantity'] - 1
                self.save()

    def clear(self):
        """Удаление корзины из сессии. Полное очищение."""

        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_price(self):
        """Подсчет стоимости товаров в корзине."""

        total = 0

        for item in self.cart.values():
            if type(item) != int:
                total += sum(float(list_item['price']) * float(list_item['quantity']) for list_item in item)

        return total

    def __iter__(self):
        """Перебор элементов в корзине и получение продуктов из базы данных."""

        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(slug__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Выводит количество товаров к корзине."""

        return sum(item['quantity'] for item in self.cart['products'])
