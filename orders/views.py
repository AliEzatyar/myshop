from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from cart.cart import Cart
from orders.forms import OrderForm
from orders.models import OrderItem, Order
from django.utils import timezone as tz
import datetime


def checkout(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # preventing multiple same order
            _10_min_ago = tz.now() - datetime.timedelta(minutes=10)
            similiars = Order.objects.filter(created__gte=_10_min_ago,
                                             first_name=request.POST['first_name'],
                                             last_name=request.POST['last_name'])
            if similiars.count() > 0:
                return render(request, "order_created.html", {'already': "1"})
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         quantity=item['quantity'],
                                         price=item['price']
                                         )
            cart.clear()
            return render(request, 'order_created.html',
                          {'order': order})
    else:
        form = OrderForm()
    return render(request, "create_order.html",
                  {'order_form': form})
