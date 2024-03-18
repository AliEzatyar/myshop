from cart.cart import Cart


def cart_in_context(request):
    """adds the cart variable in global variables"""
    print("sssssssssssssssssssssssssssssss")
    return {'the_cart': Cart(request)}
