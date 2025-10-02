from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField

from catalog.models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        exclude = ("owner",)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise ValidationError(
                    f'Недопустимое слово в названии продукта: "{word}".'
                )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        for word in FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise ValidationError(
                    f'Недопустимое слово в описании продукта: "{word}".'
                )
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        elif price == 0:
            raise ValidationError("Проверьте цену продукта.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Размер изображения не должен превышать 5 МБ.")

            valid_mime_types = ["image/jpeg", "image/png"]
            if (
                hasattr(image, "content_type")
                and image.content_type not in valid_mime_types
            ):
                raise ValidationError(
                    "Разрешены только изображения форматов JPEG и PNG."
                )

        return image


class ProductModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ("status",)
