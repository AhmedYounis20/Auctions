from django import forms
from .models import listing
class creatinglistform(forms.ModelForm):
    class Meta:
        model = listing
        fields=['productname','productdescription','productcategory','product_price','product_image_url',]
        widgets={
            'productname':forms.TextInput(attrs={'class':'form-control'}),
            'productdescription':forms.Textarea(attrs={'class':'form-control'}),
            'productcategory':forms.TextInput(attrs={'class':'form-control'}),
            'product_price':forms.TextInput(attrs={'class':'form-control'}),
            'product_image_url':forms.TextInput(attrs={'class':'form-control'}),




        }