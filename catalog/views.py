from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product, Contacts


# Create your views here.
def home(request):
    last_products = Product.objects.order_by("-id")[:5]
    print("Последние 5 созданных продуктов:")
    for product in last_products:
        print(f"{product.name}")
    return render(request, "catalog/home.html", {'latest_products': last_products})


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        Contacts.objects.create(name=name, phone=phone, message=message)
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    contact_list = Contacts.objects.all()
    return render(request, "catalog/contacts.html", {"contacts": contact_list})
