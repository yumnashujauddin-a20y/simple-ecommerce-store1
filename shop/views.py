
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

from .models import Product, Order, OrderItem
from .forms import RegisterForm, CheckoutForm


def home(request):
    query = request.GET.get("q", "").strip()

    if query:
        products = Product.objects.filter(
            name__icontains=query
        ).order_by("-created_at")
    else:
        products = Product.objects.all().order_by("-created_at")

    return render(
        request,
        "shop/home.html",
        {
            "products": products,
            "query": query,
        }
    )


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(
        request,
        "shop/product_detail.html",
        {
            "product": product,
        }
    )


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})
    product_id_str = str(product_id)

    cart[product_id_str] = int(cart.get(product_id_str, 0)) + 1

    request.session["cart"] = cart
    request.session.modified = True

    messages.success(
        request,
        f"{product.name} added to cart."
    )

    return redirect("cart")


def cart(request):
    cart_data = request.session.get("cart", {})

    cart_items = []
    total = 0

    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, id=product_id)

        quantity = int(quantity)
        item_total = product.price * quantity
        total += item_total

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "item_total": item_total,
        })

    return render(
        request,
        "shop/cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )


def update_cart(request, product_id):
    cart_data = request.session.get("cart", {})
    product_id_str = str(product_id)

    action = request.GET.get("action")

    if product_id_str in cart_data:
        quantity = int(cart_data[product_id_str])

        if action == "increase":
            quantity += 1

        elif action == "decrease":
            quantity -= 1

        if action in ("increase", "decrease"):
            if quantity > 0:
                cart_data[product_id_str] = quantity
            else:
                cart_data.pop(product_id_str, None)

            request.session["cart"] = cart_data
            request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, product_id):
    cart_data = request.session.get("cart", {})
    product_id_str = str(product_id)

    if product_id_str in cart_data:
        cart_data.pop(product_id_str)

    request.session["cart"] = cart_data
    request.session.modified = True

    return redirect("cart")


@login_required
def checkout(request):
    cart_data = request.session.get("cart", {})

    if not cart_data:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart")

    cart_items = []
    total = 0

    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, id=product_id)

        quantity = int(quantity)
        item_total = product.price * quantity
        total += item_total

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "item_total": item_total,
        })

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                address=form.cleaned_data["address"],
                phone=form.cleaned_data["phone"],
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["product"].price,
                )

            request.session["cart"] = {}
            request.session.modified = True

            return render(
                request,
                "shop/order_success.html",
                {
                    "order": order,
                }
            )
    else:
        form = CheckoutForm()

    return render(
        request,
        "shop/checkout.html",
        {
            "form": form,
            "cart_items": cart_items,
            "total": total,
        }
    )


@login_required
def orders(request):
    user_orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "shop/orders.html",
        {
            "orders": user_orders,
        }
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("home")
    else:
        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        }
    )
