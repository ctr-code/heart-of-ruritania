from django import forms
from .models import Dish


class DishForm(forms.ModelForm):
    """
    Form for creating and editing menu dishes
    """
    class Meta:
        model = Dish
        fields = ('name', 'description', 'price', 'active')
