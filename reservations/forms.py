from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    """
    The Reservation form is used to get the guest count when creating or
    editing a reservation
    """
    class Meta:
        model = Reservation
        fields = ('guest_count', )
