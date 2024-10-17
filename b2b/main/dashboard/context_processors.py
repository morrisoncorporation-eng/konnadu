from main.cart.models import Cart
# from django.contrib.auth.decorators import login_required



def new_arrival(request):
    if request.user.is_authenticated:
        try:
            new_cart_arrival = Cart.objects.filter(status="pending")
            return {"new_cart_arrival": new_cart_arrival }
        except Exception as e:
            return ''

    else: 
        return ''
