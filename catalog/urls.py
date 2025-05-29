from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ContactsView, ProductDetailView, ProductCreateView, CatalogListView, ProductUpdateView, \
    ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", CatalogListView.as_view(), name="home"),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path("product/<int:pk>/detail/", ProductDetailView.as_view(), name="product_detail"),
    path("new/", ProductCreateView.as_view(), name="add_product"),
    path("product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
