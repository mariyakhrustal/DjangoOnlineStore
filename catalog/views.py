from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from catalog.models import Product, Contacts


# Create your views here.
def home(request):
    all_products = Product.objects.order_by('-id')
    paginator = Paginator(all_products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    last_products = Product.objects.order_by("-id")[:5]
    print("Последние 5 созданных продуктов:")
    for product in last_products:
        print(f"{product.name}")
    context = {"products": page_obj}
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
