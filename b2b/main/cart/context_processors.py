from main.cart.models import Cart


def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(owner=request.user)
        return {'cart': cart}
    else:
        return {'cart': 0 }