from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "store"

urlpatterns = [

                  # Обработка шаблонов.
                  path('', views.index, name="index"),
                  path('profile/<slug:slug>/', views.profile, name='profile'),

                  path('add_to_favorite/<slug:product_slug>/', views.add_to_favorite, name='add_to_favorite'),
                  path('remove_from_favorite/<slug:product_slug>/', views.remove_from_favorite,
                       name='remove_from_favorite'),

                  path('product_detail/<slug:product_slug>/', views.product_detail, name='product_detail'),
                  path('products_by_category/<int:category_pk>/', views.products_list_by_category,
                       name='products_by_category'),

                  path('order_detail/<int:order_pk>/', views.order_detail, name='order_detail'),
                  path('create_order/', views.create_order, name='create_order'),

                  path('register/', views.register_user, name='register'),
                  path('login/', views.login_user, name='login'),
                  path('logout/', views.logout_user, name='logout')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
