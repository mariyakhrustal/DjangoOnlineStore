from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.CharField(
        max_length=250,
        verbose_name="Заголовок",
        help_text="Введите заголовок блоговой записи",
    )
    content = models.TextField(
        verbose_name="Контент",
        help_text="Введите контент для блоговой записи",
    )
    preview_image = models.ImageField(
        upload_to="preview_image/",
        verbose_name="Фото",
        null=True,
        blank=True,
        help_text="Загрузите фото для блоговой записи",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    is_congratulated = models.BooleanField(
        default=False, verbose_name="Отправлено поздравительное письмо"
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    view_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
