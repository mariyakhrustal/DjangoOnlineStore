from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from catalog.models import Product, Contacts, Category
from catalog.forms import ProductForm, ProductModeratorForm
from catalog.services import get_products_by_category, get_all_cached_products


class CategoryProductsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs["category_id"]
        context["categories"] = Category.objects.all()
        context["current_category"] = get_object_or_404(Category, id=category_id)
        return context


class DraftListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/product_drafts.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.filter(status="draft").order_by("-created_at")
        return Product.objects.filter(status="draft", owner=user).order_by(
            "-created_at"
        )


class CatalogListView(ListView):
    model = Product
    paginate_by = 6
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return get_all_cached_products()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


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

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        if user == obj.owner or user.has_perm("catalog.delete_product"):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied
