from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from config.settings import DEFAULT_FROM_EMAIL
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        self.send_welcome_email(self.object.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать в наш сервис Juicy Corner!"
        message = "Спасибо, что зарегистрировались в нашем сервисе!"
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"

    def get_object(self, queryset=None):
        return self.request.user

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile")  # после сохранения вернёт на страницу профиля

    def get_object(self, queryset=None):
        return self.request.user  # редактируем только свой профиль
