from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main.customer.models import Customer
from .forms import AddressForm
from django.contrib import messages
from .models import Address


@login_required
def address_list(request):
    customer = Customer.objects.get(user=request.user)

    addresses = Address.objects.filter(customer=customer)
    return render(request, "address/list", {"addresses": addresses})

@login_required
def address_create(request):
    customer = Customer.objects.get(user=request.user)
    addresses = Address.objects.filter(customer=customer)
    form = AddressForm()
    if request.method == "POST":
        form = AddressForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.customer = customer
            instance.save()
            messages.add_message(request, messages.SUCCESS, "Address added!")
            return redirect("address:address_create")
        else:
            return render(request, "address/create.html", {"form":form})
    return render(request, "address/create.html", {"form": form, "addresses": addresses})


@login_required
def set_default_address(request):
    if request.method == "POST":
        customer = Customer.objects.get(user=request.user)
        address_id = request.POST.get("address_id")
        addresses = Address.objects.filter(customer=customer)
        for add in addresses:
            add.default = False
            add.save()
        address = Address.objects.get(id=address_id)
        address.default = True
        address.save()
        messages.add_message(request, messages.SUCCESS, "Address set as default!")
        return redirect("address:address_create")
