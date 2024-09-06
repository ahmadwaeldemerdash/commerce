from django import forms 
from .models import Category
categories = [("", "-------")]
c = Category.objects.all()
for i in c :
    
    categories.append((i.id, i.Category))

class Form(forms.Form):
    
    title = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    category = forms.ChoiceField(choices=categories, widget=forms.Select(attrs={'class' : 'form-control'}), required=False)
    description = forms.CharField(max_length=5000, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    price = forms.FloatField(min_value=0, max_value=5000, widget=forms.NumberInput(attrs={'class' : 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class' : 'form-control'}), required=False)


class bid_form(forms.Form):
    user_bid = forms.FloatField(label='',min_value=1, max_value=10000, widget=forms.NumberInput(attrs={"class" : "form-control", "placeholder" : "Bid"}))