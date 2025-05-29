from django.urls import path
from my_blog.apps import MyBlogConfig
from my_blog.views import MyBlogListView, MyBlogDetailView, MyBlogCreateView, MyBlogUpdateView, MyBlogDeleteView


app_name = MyBlogConfig.name

urlpatterns = [
    path("blogs/", MyBlogListView.as_view(), name="blogs"),
    path("blogs/<int:pk>/", MyBlogDetailView.as_view(), name="blogs_detail"),
    path("blogs/create/", MyBlogCreateView.as_view(), name="blogs_create"),
    path("blogs/<int:pk>/edit/", MyBlogUpdateView.as_view(), name="blogs_update"),
    path("blogs/<int:pk>/delete/", MyBlogDeleteView.as_view(), name="blogs_delete"),
]