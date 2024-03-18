from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.decorators.http import require_POST

from orders.models import OrderItem
from shop.models import Product
from .cart import Cart
from .forms import AddProductCartForm


@require_POST
def cart_add(request, product_id):
    """adds or updates a product on the cart"""
    product = Product.objects.get(id=product_id)
    add_form = AddProductCartForm(request.POST)
    cart = Cart(request)
    if add_form.is_valid():
        cd = add_form.cleaned_data
        cart.add(product, cd['quantity'], cd['override_quantity'])
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    """removes a product from the cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update'] = AddProductCartForm(initial={'quantity': item['quantity'],
                                                     'override_quantity': True})

    return render(request, "cart_detail.html", {'cart': cart})


