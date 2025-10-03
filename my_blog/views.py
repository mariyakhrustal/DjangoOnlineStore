from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from my_blog.models import Blog


class MyBlogListView(ListView):
    model = Blog
    ordering = ["-created_at"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newest_post"] = self.object_list.first()
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        return queryset


class MyBlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        if obj.view_count >= 100 and not obj.is_congratulated:
            # Отправка письма
            send_mail(
                subject="Ура! 100 просмотров!",
                message=f'Ваша статья "{obj.title}" набрала 100 просмотров!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["your_email@example.com"],  # сюда введи свою почту
                fail_silently=False,
            )
            obj.is_congratulated = True

        obj.save(
            update_fields=["view_count", "is_congratulated"]
        )  # сохраняем только поле views
        return obj


class MyBlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ("title", "content", "preview_image", "is_published")
    success_url = reverse_lazy("my_blog:blogs")


class MyBlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ("title", "content", "preview_image", "is_published")
    success_url = reverse_lazy("my_blog:blogs")

    def get_success_url(self):
        return reverse("my_blog:blogs_detail", args=[self.kwargs.get("pk")])


class MyBlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy("my_blog:blogs")
