from django import forms


class UserForm(forms.Form):
    product_name = forms.CharField(max_length=200)
    city_name = forms.CharField(max_length=200)
    file = forms.FileField()
