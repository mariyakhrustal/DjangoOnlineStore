from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product, Contacts


# Create your views here.
class CatalogListView(ListView):
    model = Product
    ordering = ["-id"]
    paginate_by = 10


class ContactsView(View):
    def get_contacts(self):
        return Contacts.objects.order_by("-id")[:5]

    def get(self, request):
        return render(request, "catalog/contacts.html", {"contacts": self.get_contacts()})

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        Contacts.objects.create(name=name, phone=phone, message=message)
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = ("name", "category", "description", "image", "price")
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(UpdateView):
    model = Product
    fields = ("name", "category", "description", "image", "price")
    success_url = reverse_lazy("catalog:home")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")
