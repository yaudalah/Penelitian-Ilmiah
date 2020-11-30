from django.views.generic import ListView, DetailView 
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, request
from django.urls import reverse_lazy

from .models import *
from .forms import ProductForm, BonForm
from django.shortcuts import render

class ProductList(ListView): 
    model = Product
    template_name = 'product/product_list.html'

class ProductDetail(DetailView): 
    model = Product
    template_name = 'product/product_detail.html'

class ProductCreate(SuccessMessageMixin, CreateView): 
    model = Product
    template_name = 'product/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    success_message = "Product successfully created!"

class ProductUpdate(SuccessMessageMixin, UpdateView): 
    model = Product
    template_name = 'product/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    success_message = "Product successfully updated!"

class ProductDelete(SuccessMessageMixin, DeleteView):
    model = Product
    template_name = 'product/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    success_message = "Product successfully deleted!"


class BonList(ListView): 
    model = Bon
    template_name = 'bon/bon_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a models
        context['product'] = Product.objects.all()
        context['hawker'] = Hawker.objects.all()
        return context

class BonDetail(DetailView): 
    model = Bon
    template_name = 'bon/bon_detail.html'


def BonCreate(request):
    product = Product.objects.all()
    bon = Bon.objects.all()
    hawkers = Hawker.objects.all()
    context = {'bon': bon, 'product': product, 'hawkers': hawkers}
    return render(request, 'bon/bon_form.html', context)


def SalinBarang(request):
    
    if request.method == 'POST':
        s = Sales(hawker_id=request.POST['hawker_id'])
        s.save()
        hps = HawkerProduct.objects.filter(hawker_id=s.hawker_id)

    product = Product.objects.all()
    hawkers = Hawker.objects.all()
    context = {'products': product, 'hawkers': hawkers}
    return render(request, 'bon/salinbarang.html', context)


class BonUpdate(SuccessMessageMixin, UpdateView): 
    model = Bon
    template_name = 'bon/bon_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('bon_list')
    success_message = "Bon successfully updated!"

class BonDelete(SuccessMessageMixin, DeleteView):
    model = Bon
    template_name = 'bon/bon_confirm_delete.html'
    success_url = reverse_lazy('bon_list')
    success_message = "Bon successfully deleted!"