from django import forms

from orders.models import Order

choices = [(i, str(i)) for i in range(21)]


class AddProductCartForm(forms.Form):
    quantity = forms.TypedChoiceField(coerce=int, choices=choices)
    override_quantity = forms.BooleanField(widget=forms.HiddenInput, initial=False, required=False)


