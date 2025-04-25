from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите наименование товара",
    )
    description = models.TextField(
        verbose_name="Описание",
        null=True,
        blank=True,
        help_text="Введите описание товара",
    )
    image = models.ImageField(
        upload_to="photo/",
        verbose_name="Фото",
        null=True,
        blank=True,
        help_text="Загрузите фото товара",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name="Категория",
        help_text="Введите категорию товара",
        related_name="products",
    )
    price = models.FloatField(
        verbose_name="Цена",
        help_text="Введите цену товара",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание",
        null=True,
        blank=True,
        help_text="Введите описание категории",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
