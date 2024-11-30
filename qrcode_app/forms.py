from django import forms

class QRCodeForm(forms.Form):
    restaurant_name = forms.CharField(
        max_length=50,
        label="Restaurant Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter the restaurant's name",
                "class": "form-control"
            }
        )
    )
    url = forms.URLField(
        max_length=200,
        label="Menu URL",
        widget=forms.URLInput(
            attrs={
                "placeholder": "Enter the restaurant's name",
                "class": "form-control"
            }
        )
        )
