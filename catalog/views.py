from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from catalog.models import Product, Contacts


# Create your views here.
def home(request):
    last_products = Product.objects.order_by("-id")[:5]
    all_products = Product.objects.all()
    context = {"products": all_products}
    print("Последние 5 созданных продуктов:")
    for product in last_products:
        print(f"{product.name}")
    return render(request, "catalog/home.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        Contacts.objects.create(name=name, phone=phone, message=message)
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    last_contacts = Contacts.objects.order_by("-id")[:5]
    return render(request, "catalog/contacts.html", {"contacts": last_contacts})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "catalog/product_detail.html", context)
