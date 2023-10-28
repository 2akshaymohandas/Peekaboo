from django import forms
from accounts.models import CustomUser
from cart.models import Coupon
    



class Aforms(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields=['email','name','password']
        widgets={
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(render_value=True,attrs={'class':'form-control'}),
        }



class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'is_expired', 'discount_price', 'minimum_amount']
        widgets = {
            'coupon_code': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            # 'is_expired': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'is_expired': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'minimum_amount': forms.DateInput(attrs={'class': 'form-control datepicker mb-3'}),
            
        }


class DateFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))