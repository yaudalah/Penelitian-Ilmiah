# -*- coding: utf-8 -*-
from django import forms

from .models import *

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'form-control col-md-6'
        }
        # self.fields['description'].widget.attrs = {
        #     'class': 'form-control col-md-6'
        # }
        self.fields['price'].widget.attrs = {
            'class': 'form-control col-md-6',
            'step': 'any',
            'min': '1',
        }
        self.fields['stock'].widget.attrs = {
            'class': 'form-control col-md-6',
            'step': 'any',
            'min': '1',
        }
    class Meta:
        model = Product
        fields = ('name', 'price', 'stock')
    
class BonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BonForm, self).__init__(*args, **kwargs)
        self.fields[{{Hawker.name}}].widget.attrs = {
            'class': 'custom-select mr-sm-2'
        }
        
        # self.fields['hawker_stock'].widget.attrs = {
        #     'class': 'form-control col-md-6',
        #     'step': 'any',
        #     'min': '1',
        # }