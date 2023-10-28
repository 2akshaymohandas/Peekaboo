from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from image_cropping import ImageCropWidget


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_name", "Brand","Category", "discription", "price", "gender", "image", "is_available", "cropping"]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'Brand': forms.Select(attrs={'class': 'form-control mb-3'}),
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
            'discription': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'cropping': ImageCropWidget(attrs={'class': 'form-control mb-3'}),
            # 'stock': forms.NumberInput(attrs={'class': 'form-control mb-3'})
            # 'image': forms.ClearableFileInput(attrs={'multiple': True}),
            
        }
    image = forms.ImageField(label='Product Image', required=True, error_messages={'required': 'Please upload an image.'})
    

class VariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product_name', 'size', 'stock', 'price']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields=['category_name']


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields=['brand_name']


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields=['name']


# class ColorForm(forms.ModelForm):
#     class Meta:
#         model = Color
#         fields=['name']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product_name','image']