from django.views.generic import ListView, DetailView 
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, request
from django.urls import reverse_lazy
from .models import *
from .forms import ProductForm, BonForm
from django.shortcuts import render
from django.db import transaction
from django.utils import timezone

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


STATE_BON_NOT_CREATED = 0
STATE_BON_ISI_BARANG = 1
STATE_BON_SETORAN = 2
STATE_BON_SELESAI = 3

def TodayTransaction(request):

    if (request.method == 'POST'):
        postHandler(request)
        
    hawkers = Hawker.objects.all().values('id', 'name')
    hawker_id = int(request.GET.get('hawker_id') if request.GET.get('hawker_id') else 0)
    
    now = timezone.now()
    sales = Sales.objects.filter(date__date=now, hawker_id=hawker_id).only('id', 'total').first() if hawker_id > 0 else None
    state = sales.state if sales else STATE_BON_NOT_CREATED

    formContext = {}
    if state is STATE_BON_ISI_BARANG:
        formContext = getProductsAndHawkerProducts(hawker_id)
    if state is STATE_BON_SETORAN or state is STATE_BON_SELESAI:
        formContext = getSalesProducts(sales.id) 


    ctx = {
        'date': timezone.localtime(now).strftime("%d/%m/%Y"),
        'hawkers':hawkers, 
        'selected_hawker_id': hawker_id, 
        'form_state': state,
        'option_state': {
            'not_created': STATE_BON_NOT_CREATED,
            'isi_barang': STATE_BON_ISI_BARANG,
            'setoran': STATE_BON_SETORAN,
            'selesai': STATE_BON_SELESAI
        },
        'sales': sales,
        **formContext
    }

    return render(request, 'transaction/today.html', ctx)


def postHandler(request):
    input_form_state = int(request.POST.get('form_state'))
    hawker_id = int(request.POST.get('hawker_id'))
        
    if input_form_state == STATE_BON_NOT_CREATED:
        salinBon(hawker_id)

    if input_form_state == STATE_BON_ISI_BARANG:
        sales_id = int(request.POST.get('sales_id'))
        product_ids = request.POST.getlist('product_id[]')
        added_stock = request.POST.getlist('product_add_stock[]')
        input_products = dict(zip(product_ids, added_stock))

        IsiBarang(sales_id, input_products)

    if input_form_state == STATE_BON_SETORAN:
        sales_id = int(request.POST.get('sales_id'))
        product_ids = request.POST.getlist('product_id[]')
        product_leftover = request.POST.getlist('product_leftover[]')
        input_products = dict(zip(product_ids,product_leftover))

        Setoran(hawker_id, sales_id, input_products)


             

@transaction.atomic
def salinBon(hawker_id):
    today_sales = Sales.objects.create(hawker_id=hawker_id, date=timezone.now(), state=STATE_BON_ISI_BARANG)
    hawker_products = HawkerProduct.objects.filter(hawker_id=hawker_id)

    for hp in hawker_products:
        SalesProduct.objects.create(sales_id=today_sales.id, product_id=hp.product_id, initial_stock=hp.stock)



@transaction.atomic
def IsiBarang(sales_id, input_products):
    for product_id, added_stock in input_products.items():
        db_product = Product.objects.only('stock').get(pk=product_id)

        if not added_stock or int(added_stock) < 1 or db_product.stock < int(added_stock):
            continue
        
        SalesProduct.objects.update_or_create(sales_id=sales_id, product_id=product_id, defaults={'add_stock': added_stock})
      
        db_product.stock = db_product.stock - int(added_stock)
        db_product.save()
    
    Sales.objects.filter(pk=sales_id).update(state=STATE_BON_SETORAN)




@transaction.atomic
def Setoran(hawker_id, sales_id, input_products):
    grand_total = 0

    for product_id, total_leftover in input_products.items():
        product = Product.objects.only('price').get(pk=product_id) 
        db_sales_prod = SalesProduct.objects.filter(sales_id=sales_id, product_id=product_id).first()

        total_stock = db_sales_prod.initial_stock + db_sales_prod.add_stock
        sold = total_stock - int(total_leftover)

        db_sales_prod.sold = sold
        db_sales_prod.price_per_product = product.price
        db_sales_prod.total =  product.price * sold
        db_sales_prod.save()

        grand_total += db_sales_prod.total
     
        HawkerProduct.objects.update_or_create(
            hawker_id=hawker_id, product_id=product_id, defaults={'stock': total_leftover},
        )
    

    Sales.objects.filter(pk=sales_id).update(state=STATE_BON_SELESAI, total=grand_total)


def getProductsAndHawkerProducts(hawker_id):
    products = Product.objects.all() 
    hawker_products = HawkerProduct.objects.filter(hawker_id=hawker_id).only('product_id', 'stock')
    hawker_stock_map = {}
    for hp in hawker_products:
        hawker_stock_map[hp.product_id] = hp.stock

    return {
        'products': products,
        'hawker_stock_map': hawker_stock_map
    }

def getSalesProducts(sales_id):
    sales_details = SalesProduct.objects.filter(sales_id=sales_id).select_related('product')
   
    return {
        'sales_details': sales_details,
    }
