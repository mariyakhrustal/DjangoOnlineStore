from django.core.exceptions import ValidationError
from django.forms import ModelForm

from catalog.models import Product

FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        # fields = ("name", "category", "description", "image", "price")

    def clean_name(self):
        name = self.cleaned_data.get("name")
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise ValidationError(f'Недопустимое слово в названии продукта: "{word}".')
        return name


    def clean_description(self):
        description = self.cleaned_data.get("description")
        for word in FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise ValidationError(f'Недопустимое слово в описании продукта: "{word}".')
        return description
