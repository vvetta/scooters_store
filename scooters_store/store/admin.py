from django.contrib import admin
from .models import User, Product, ProductsCategory, Favorite, Order, Store

# Register your models here.


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    """Подробное представление модели Заказа в админ панели сайта."""

    list_display = ['pk', 'user', 'variant', 'address', 'store', 'status', 'price', 'created_date']
    readonly_fields = ['price']
    list_filter = ['created_date', 'status']


admin.site.register(User)
admin.site.register(Product)
admin.site.register(ProductsCategory)
admin.site.register(Favorite)
admin.site.register(Store)
