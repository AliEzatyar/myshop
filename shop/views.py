from django.shortcuts import render, get_object_or_404
from cart.forms import AddProductCartForm
# Create your views here.
from shop.models import Product, Category


def show_products(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, "shop/product/list.html", {'products': products,
                                                      'categories': categories,
                                                      'category': category})


def product_detail(request, id, slug):
    form = AddProductCartForm()
    product = get_object_or_404(Product, id=id,
                                slug=slug,
                                available=True)

    return render(request, "shop/product/detail.html", {'product': product, "cart_product_form": form})
