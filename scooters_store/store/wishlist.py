from django.conf import settings
from .models import Product


class WishList(object):
    """Список желаемого, хранящийся в сессии."""

    def __init__(self, request):
        """Инициализируем список желаемого"""

        self.session = request.session
        wishlist = self.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            # save an empty cart in the session
            wishlist = self.session[settings.WISHLIST_SESSION_ID] = {'products': []}
        self.wishlist = wishlist

    def add(self, product: Product):
        """Добавляет товар в избранное."""

        product_id = str(product.slug)

        if product_id not in [item['slug'] for item in self.wishlist['products']]:
            self.wishlist['products'].append({'price': str(product.price), 'title': product.title,
                                              'description': product.description, 'slug': product.slug,
                                              'photo': str(product.photo), 'quantity': 1})

        self.save()

    def save(self):
        """Сохраняет список желаемого."""

        # Обновление сессии cart
        self.session[settings.WISHLIST_SESSION_ID] = self.wishlist

        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины."""

        product_id = str(product.slug)
        for product in self.wishlist['products']:
            if product['slug'] == product_id:
                self.wishlist['products'].remove(product)

        self.save()
