from django import forms
from .models import CompressImage


class CompressImageForm(forms.ModelForm):
    original_img = forms.ImageField(label="Upload an Image")
    class Meta:
        model = CompressImage
        fields = ('original_img', 'quality')