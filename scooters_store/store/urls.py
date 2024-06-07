from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "store"

urlpatterns = [

                  # Обработка шаблонов.
                  path('', views.index, name="index"),
                  path('profile/<slug:user_slug>/', views.profile, name='profile'),
                  path('update_profile/', views.update_user, name="update_profile"),

                  path('add_to_favorite/<slug:product_slug>/', views.add_to_favorite, name='add_to_favorite'),
                  path('remove_from_favorite/<slug:product_slug>/', views.remove_from_favorite,
                       name='remove_from_favorite'),
                  path('wishlist_detail/', views.wishlist_detail, name="wishlist_detail"),

                  path('product_detail/<slug:product_slug>/', views.product_detail, name='product_detail'),
                  path('products_by_category/<int:category_pk>/', views.products_list_by_category,
                       name='products_by_category'),

                  path('create_order/', views.create_order, name='create_order'),

                  path('get_cart/', views.cart_detail, name='cart_detail'),
                  path('add_to_cart/<slug:product_slug>/', views.cart_add, name='cart_add'),
                  path('remove_from_cart/<slug:product_slug>/', views.cart_remove, name='cart_remove'),
                  path('clean_cart/', views.clean_cart, name='cart_clean'),



                  path('register/', views.register_user, name='register'),
                  path('login/', views.login_user, name='login'),
                  path('logout/', views.logout_user, name='logout')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
