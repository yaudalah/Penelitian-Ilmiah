from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from members.models import Hawker

class Product(models.Model):
    letters = RegexValidator(r'^[a-z A-Z]*$', 'Only alphanumeric characters are allowed.')
    name = models.CharField('Name', max_length=100, validators=[letters], unique=True)
    description = models.TextField('Description', default='-', blank=True)
    price = models.DecimalField('Price', decimal_places=2, max_digits=8)
    stock = models.IntegerField('Stock', default=0,
        validators= [MinValueValidator(0), MaxValueValidator(1000)]
    )
    created = models.DateTimeField('Created', auto_now_add=True)
    changed = models.DateTimeField('Changed', auto_now=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('product_edit', kwargs={'pk': self.pk})

class HawkerProduct(models.Model):
    hawker = models.ForeignKey(Hawker, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField('Stock', default=0,
        validators= [MinValueValidator(0), MaxValueValidator(1000)]
    )
class Sales(models.Model):
    hawker = models.ForeignKey(Hawker, on_delete=models.CASCADE)
    date = models.DateTimeField('date sale', auto_now_add=True, unique=True)

class SalesProduct(models.Model):
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    initial_stock = models.IntegerField('Sold', default=0,
        validators= [MinValueValidator(0), MaxValueValidator(1000)]
    )
    add_stock = models.IntegerField('Sold', default=0,
        validators= [MinValueValidator(0), MaxValueValidator(1000)]
    )
    sold = models.IntegerField('Sold', default=0,
        validators= [MinValueValidator(0), MaxValueValidator(1000)]
    )
    price_per_product = models.DecimalField('Price per Product', decimal_places=2, max_digits=8)
    total = models.DecimalField('Price Total', decimal_places=2, max_digits=8)


class Purchase(models.Model):
    date = models.DateTimeField('date purchased', auto_now_add=True)

    def __str__(self):
        return self.date

    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) <= self.date <= now

class Bon(models.Model):
    hawker = models.ForeignKey(Hawker,on_delete=models.CASCADE)
    hawker_stock = models.IntegerField('Hawker Stock', default=0,
        validators= [MinValueValidator(0), MaxValueValidator(1000)]
    )

    created = models.DateTimeField('Created', auto_now_add=True)
    changed = models.DateTimeField('Changed', auto_now=True)

    def get_absolute_url(self):
        return reverse('bon_edit', kwargs={'pk': self.pk})



