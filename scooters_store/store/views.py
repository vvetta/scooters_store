from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import JsonResponse
from .models import User, Product, Favorite, ProductsCategory, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request, category_pk: int | None = None):
    """Представление главное страницы."""

    category = None

    # Выводим только активные товары, и товары, у которых количество больше 0.
    products = Product.objects.filter(is_active=True, count__gt=0)
    categories = ProductsCategory.objects.all()

    if category_pk:
        category = get_object_or_404(ProductsCategory, pk=category_pk)
        products = products.filter(categories=category)

    context = {
        'products': products,
        'categories': categories,
        'category': category
    }

    return render(request, '', context=context)


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

    return render(request, '', context=context)


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
            'product': product
        }

    return render(request, '', context=context)


def register_user(request):
    """Представление регистрации пользователя."""

    if request.method == "POST":
        email = request.get['email']
        password = request.get['password']

        user = User(email=email, password=password)

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
        email = request.get['email']
        password = request.get['password']

        user = authenticate(username=email, password=password)

        if not user:
            return JsonResponse({'message': 'Вы ввели неверные данные или такого пользователя не существует!',
                                 'status_code': 403})

        if user.is_active:
            login(request, user)
            return JsonResponse({'message': 'Вы успешно авторизовались!',
                                 'status_code': 200})


def logout_user(request):
    """Представление выхода пользователя из системы."""

    logout(request)


# Надо доделать!!!!!!!!!
def create_order(request):
    """Представление создающее заказ."""

    # Сделать подсчёт стоимости, сложив стоимость каждого товара.

    if request.method == "POST":
        products = [Product.objects.filter(slug=product['slug']) for product in request.get['products']]

        order = Order(products=products)

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
