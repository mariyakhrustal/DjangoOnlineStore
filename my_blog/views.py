from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from my_blog.models import Blog

# Create your views here.
class MyBlogListView(ListView):
    model = Blog
    ordering = ['-created_at']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newest_post'] = self.object_list.first()
        return context


class MyBlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save(update_fields=['view_count'])  # сохраняем только поле views
        return obj

class MyBlogCreateView(CreateView):
    model = Blog
    fields = ("title", "content", "preview_image", "is_published")
    success_url = reverse_lazy("my_blog:blogs")


class MyBlogUpdateView(UpdateView):
    model = Blog
    fields = ("title", "content", "preview_image", "is_published")
    success_url = reverse_lazy("my_blog:blogs")


class MyBlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy("my_blog:blogs")
