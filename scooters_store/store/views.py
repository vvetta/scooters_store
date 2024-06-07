from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password
from django.http.response import JsonResponse
from .models import User, Product, Favorite, ProductsCategory, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .cart import Cart
from .wishlist import WishList
import json


# Create your views here.


def index(request):
    """Представление главное страницы."""

    # Выводим только активные товары, и товары, у которых количество больше 0.
    new_products = Product.objects.filter(is_active=True, count__gt=0, new=1)
    top_sale_products = Product.objects.filter(is_active=True, count__gt=0, top_sale=1)

    categories = ProductsCategory.objects.all()

    context = {
        'new_products': new_products,
        'top_sale_products': top_sale_products,
        'categories': categories,
    }

    return render(request, 'index.html', context=context)



def profile(request, user_slug: str):
    """Представление профиля пользователя."""

    user = get_object_or_404(User, slug=user_slug)
    favorites_list = Favorite.objects.filter(user=user)
    orders_list = Order.objects.filter(user=user)
    categories = ProductsCategory.objects.all()

    context = {
        'user': user,
        'favorites_list': favorites_list,
        'orders_list': orders_list,
        'categories': categories
    }

    return render(request, 'profile.html', context=context)


def update_user(request):
    """Обновляет данные пользователя."""

    if request.method == "POST" and request.user.is_authenticated:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        city = request.POST.get('city')
        phone = request.POST.get('phone')

        user_for_update = User.objects.get(email=request.user.email)

        user_for_update.first_name = first_name
        user_for_update.last_name = last_name
        user_for_update.city = city
        user_for_update.phone = phone

        user_for_update.save()

        return redirect(f'http://127.0.0.1:8081/profile/{user_for_update.slug}/')




def product_detail(request, product_slug):
    """Представление детальной информации о товаре."""

    product = get_object_or_404(Product, slug=product_slug)
    categories = ProductsCategory.objects.all()

    context = {
        'product': product,
        'categories': categories
    }

    return render(request, 'product_detail.html', context=context)


def products_list_by_category(request, category_pk: int):
    """Возвращает товары по выбранной категории."""

    category = ProductsCategory.objects.get(pk=category_pk)
    products = Product.objects.filter(categories=category)
    categories = ProductsCategory.objects.all()

    return render(request, 'products_by_categories.html', {'products': products,
                                                           'categories': categories,
                                                           'actual_category': category})


def register_user(request):
    """Представление регистрации пользователя."""

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User(email=email, password=make_password(password))

        try:
            user.save()
            return redirect('/')
        except Exception as e:
            return JsonResponse({'message': 'Произошла ошибка при попытке создать пользователя!',
                                 'status_code': 403})


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

        data = json.loads(request.body)

        products = [Product.objects.get(slug=request_product) for request_product in data['products']]

        order = Order(price=data['total_price'], address=data['address'],
                      first_name=data['first-name'], last_name=data['last-name'], city=data['city'],
                      phone=data['tel'], email=data['email'], comment=data['comment'])

        if request.user.is_authenticated:
            order.user = request.user

        order.save()
        order.products.set(products)

        try:
            order.save()
            return JsonResponse({'message': 'Ваш заказ успешно создан, ожидайте звонка на указанный телефон!',
                                 'status_code': 200,
                                 'order_id': order.pk})
        except Exception as e:
            return JsonResponse({'message': 'При попытке совершить заказ произошла ошибка! Повторите попытку позже!',
                                 'status_code': 403,
                                 'error_detail': e})

    if request.method == "GET":
        categories = ProductsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'order_create_page.html', context=context)


@require_POST
def add_to_favorite(request, product_slug: str):
    """Представление добавления товара в избранное."""

    wishlist = WishList(request)
    product = get_object_or_404(Product, slug=product_slug)
    wishlist.add(product)

    return JsonResponse(wishlist.wishlist)


@require_POST
def remove_from_favorite(request, product_slug: str):
    """Представление, удаляющее товар из избранного."""

    wishlist = WishList(request)
    product = get_object_or_404(Product, slug=product_slug)
    wishlist.remove(product)

    return JsonResponse(wishlist.wishlist)


def wishlist_detail(request):
    """Возвращает список желаемого."""

    wishlist = WishList(request)
    return JsonResponse(wishlist.wishlist)


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
    cart.cart['product_len'] = len(cart)

    return JsonResponse(cart.cart)


@require_POST
def clean_cart(request):
    """Представление очищающие корзину."""

    cart = Cart(request)
    cart.clear()

    return JsonResponse(cart.cart)
