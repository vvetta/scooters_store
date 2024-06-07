from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    """Собственная модель пользователя."""

    email = models.EmailField(verbose_name="Эл. почта", unique=True, blank=False,
                              help_text="Используйте формат: name@domain.com.")

    first_name = models.CharField(verbose_name="Имя", blank=True, null=True, max_length=30)
    last_name = models.CharField(verbose_name="Фамилия", blank=True, null=True, max_length=30)
    city = models.CharField(verbose_name="Город", blank=True, null=True, max_length=255)

    password = models.CharField(verbose_name="Пароль", blank=False, max_length=255)
    phone = models.CharField(verbose_name="Тел. номер", blank=True, max_length=12,
                             help_text="Используйте формат: +79770000000")
    slug = models.SlugField(verbose_name="Ссылка на профиль", unique=True)
    created_date = models.DateTimeField(verbose_name="Дата регистрации", auto_now_add=True)
    is_superuser = models.BooleanField(default=0, verbose_name="Админ")
    is_staff = models.BooleanField(default=0, verbose_name="Модератор")
    is_active = models.BooleanField(default=1, verbose_name="Активное / Нет")

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователя"

        ordering = ["-created_date"]

    def save(self, *args, **kwargs):
        """Переопределяем метод сохранения для автоматического создания поля slug из email,
        который затем становиться хеш-ключом."""

        self.slug = slugify(hash(self.email))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Собственный метод для получения ссылки на аккаунт пользователя."""
        return reverse("main:profile", kwargs={'slug': self.slug})

    def __str__(self):
        return self.email


class ProductsCategory(models.Model):
    """Модель для категорий товаров."""

    title = models.CharField(verbose_name="Наименование", blank=False, max_length=255)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    class Meta:
        verbose_name_plural = "Категории товаров"
        verbose_name = "Категорию товара"

        ordering = ["-created_date"]

    def __str__(self):
        return self.title


class Product(models.Model):
    """Модель товаров."""

    title = models.CharField(verbose_name="Наименование", blank=False, max_length=255)
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2)
    description = models.TextField(verbose_name="Описание", blank=False)
    count = models.IntegerField(verbose_name="Количество", blank=False)
    photo = models.ImageField(verbose_name="Фотография", blank=False, upload_to="media/products/")
    categories = models.ManyToManyField(ProductsCategory)
    created_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    is_active = models.BooleanField(verbose_name="Активно / Нет", default=True)
    author = models.ForeignKey(verbose_name="Кто добавил", to=User, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(verbose_name="Ссылка", unique=True)
    old_price = models.DecimalField(verbose_name="Старая цена", max_digits=10, decimal_places=2, null=True, blank=True)
    new = models.BooleanField(verbose_name="Новинка", default=0)
    top_sale = models.BooleanField(verbose_name="Лидер продаж", default=0)

    class Meta:
        verbose_name_plural = "Товары"
        verbose_name = "Товар"

        ordering = ["-created_date"]

    def save(self, *args, **kwargs):
        self.slug = slugify(hash(self.title + str(self.created_date)))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={'product_slug': self.slug})

    def __str__(self):
        return self.title


class Favorite(models.Model):
    """Модель избранных товаров."""

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    created_date = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name_plural = "Избранные товары"
        verbose_name = "Избранный товар"

        ordering = ["-created_date"]

    def __str__(self):
        return self.product.title


class Store(models.Model):
    """Модель магазинов."""

    title = models.CharField(verbose_name="Название магазина", blank=False, max_length=255)
    address = models.CharField(verbose_name="Адрес магазина", blank=False, max_length=255)
    created_date = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name_plural = "Магазины"
        verbose_name = "Магазин"

        ordering = ["-created_date"]

    def __str__(self):
        return self.title


class Order(models.Model):
    """Модель для сохранения заказов."""

    order_status = (
        ('1', 'Собирается'),
        ('2', 'Доставляется'),
        ('3', 'Доставлен в ПВЗ'),
        ('4', 'Завершён'),
        ('5', 'Отменён')
    )

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(verbose_name='Имя заказчика', null=True, blank=True, max_length=255)
    email = models.EmailField(verbose_name="Эл. почта", null=True)
    last_name = models.CharField(verbose_name='Фамилия заказчика', null=True, blank=True, max_length=255)
    city = models.CharField(verbose_name='Город заказчика', null=True, blank=True, max_length=255)
    products = models.ManyToManyField(Product, verbose_name="Товары")
    phone = models.CharField(verbose_name="Телефон", blank=True, null=True, max_length=255)
    address = models.CharField(verbose_name="Адрес доставки", null=True, max_length=255, blank=True)
    status = models.CharField(verbose_name="Статус заказа", choices=order_status, blank=False, max_length=255)
    price = models.DecimalField(verbose_name="Стоимость заказа", max_digits=10, decimal_places=2, null=True)
    comment = models.TextField(verbose_name="Комментарий к заказу", null=True, blank=True)
    created_date = models.DateTimeField(verbose_name="Дата заказа", auto_now_add=True)

    class Meta:
        verbose_name_plural = "Заказы"
        verbose_name = "Заказ"

        ordering = ["-created_date"]

    def save(self, *args, **kwargs):
        # Получает общую стоимость заказа.
        super().save(*args, **kwargs)
        self.price = sum(product.price for product in self.products.all())

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('', kwargs={'slug': self.pk})
