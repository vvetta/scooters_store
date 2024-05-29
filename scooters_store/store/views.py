from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password
from django.http.response import JsonResponse, HttpResponse
from .models import User, Product, Favorite, ProductsCategory, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .cart import Cart
from django.core import serializers


# Create your views here.


def index(request):
    """Представление главное страницы."""

    # Выводим только активные товары, и товары, у которых количество больше 0.
    products = Product.objects.filter(is_active=True, count__gt=0)
    categories = ProductsCategory.objects.all()

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'index.html', context=context)


@login_required
def profile(request, user_slug: str):
    """Представление профиля пользователя."""

    user = get_object_or_404(User, slug=user_slug)
    favorites_list = Favorite.objects.filter(user=user)
    orders_list = Order.objects.filter(user=user)

    context = {
        'user': user,
        'favorites_list': favorites_list,
        'orders_list': orders_list
    }

    return render(request, 'profile.html', context=context)


def product_detail(request, product_slug):
    """Представление детальной информации о товаре."""

    product = get_object_or_404(Product, slug=product_slug)

    if request.user.is_authenticated:
        context = {
            'product': product,
            'user': request.user
        }
    else:
        context = {
            'product': product.title
        }

    return render(request, 'product_detail.html', context=context)


def products_list_by_category(request, category_pk: int):
    """Возвращает товары по выбранной категории."""

    category = ProductsCategory.objects.get(pk=category_pk)
    products = Product.objects.filter(categories=category)

    return JsonResponse(serializers.serialize('json', products))


def register_user(request):
    """Представление регистрации пользователя."""

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User(email=email, password=make_password(password))

        try:
            user.save()
            return JsonResponse({'message': 'Пользователь успешно зарегистрирован!',
                                 'status_code': 200})
        except Exception as e:
            return JsonResponse({'message': 'Произошла ошибка при попытке создать пользователя!',
                                 'status_code': 403,
                                 'error_detail': e})


def login_user(request):
    """Представление авторизации пользователя."""

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email, password)

        user = authenticate(username=email, password=password)

        if not user:
            return JsonResponse({'message': 'Вы ввели неверные данные или такого пользователя не существует!',
                                 'status_code': 403})

        if user.is_active:
            login(request, user)
            return redirect("/")


def logout_user(request):
    """Представление выхода пользователя из системы."""

    logout(request)

    return redirect("/")


def create_order(request):
    """Представление создающее заказ."""

    if request.method == "POST":
        products = [Product.objects.filter(slug=request_product['slug']) for request_product in request.get['products']]

        order = Order(products=products, user=request.user)

        try:
            order.save()
            return redirect('')
        except Exception as e:
            return JsonResponse({'message': 'При попытке совершить заказ произошла ошибка! Повторите попытку позже!',
                                 'status_code': 403,
                                 'error_detail': e})


def order_detail(request, order_pk: int):
    """Представление просмотра информации о заказе."""

    order = get_object_or_404(Order, pk=order_pk)

    context = {
        'order': order
    }

    return render(request, '', context=context)


@login_required
def add_to_favorite(request, product_slug: str):
    """Представление добавления товара в избранное."""

    if request.method == "POST":
        product = Product.objects.get(slug=product_slug)
        favorite = Favorite(user=request.user, product=product)

        try:
            favorite.save()
            return JsonResponse({'message': 'Вы успешно добавили товар в избранное!',
                                'status_code': 200})
        except Exception as e:
            return JsonResponse({'message': 'Произошла ошибка при добавлении товара!'
                                            ' Скорее всего товар уже находится в вашем избранном!',
                                 'status_code': 403,
                                 'error_detail': e})


@login_required
def remove_from_favorite(request, product_slug: str):
    """Представление, удаляющее товар из избранного."""

    if request.method == "POST":
        product = Product.objects.get(slug=product_slug)
        favorite = Favorite.objects.get(user=request.user, product=product)

        try:
            favorite.delete()

            return JsonResponse({'message': 'Вы успешно удалили товар из избранного!',
                                 'status_code': 200})
        except Exception as e:
            return JsonResponse({'message': 'Произошла ошибка при удалении товара из избранного!'
                                            ' Возможно товар уже был удалён!',
                                 'status_code': 403,
                                 'error_detail': e})


@require_POST
def cart_add(request, product_slug: str):
    """Представление добавляющее товар в корзину."""

    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)

    cart.add(product)
    cart.cart['total_price'] = int(cart.get_total_price())

    return JsonResponse(cart.cart)


@require_POST
def cart_remove(request, product_slug: str):
    """Представление удаляющее товар из корзины."""

    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    cart.remove(product)

    cart.cart['total_price'] = int(cart.get_total_price())

    return JsonResponse(cart.cart)


def cart_detail(request):
    """Представление выводящее корзину покупок на страницу"""

    cart = Cart(request)
    cart.cart['total_price'] = int(cart.get_total_price())

    return JsonResponse(cart.cart)


@require_POST
def clean_cart(request):
    """Представление очищающие корзину."""

    cart = Cart(request)
    cart.clear()

    return JsonResponse(cart.cart)
