from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product, Contacts
from catalog.forms import ProductForm


class CatalogListView(ListView):
    model = Product
    ordering = ["-id"]
    paginate_by = 10


class ContactsView(View):
    def get_contacts(self):
        return Contacts.objects.order_by("-id")[:5]

    def get(self, request):
        return render(
            request, "catalog/contacts.html", {"contacts": self.get_contacts()}
        )

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        Contacts.objects.create(name=name, phone=phone, message=message)
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")
