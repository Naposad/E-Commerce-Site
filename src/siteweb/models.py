from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

choix=(("en attente","en attente"),
       ("payée","payée"),
       ("expédiée","expédiée"),
       ("livrée","livrée")
       )


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.name


class Products(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    slug = models.CharField(max_length=100, unique=True, blank=True)
    status = models.BooleanField(default=True)
    date_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)




"""class CommandProducts(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price
"""


class Order(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    is_actif = models.BooleanField(default=True)
    date_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'panier de : {self.user}'


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f' produit : {self.products.name}     quantité : {self.quantity}'


    def get_totale_price(self):
        return self.quantity * self.products.price



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Command(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=choix, max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *agrs, **kwargs):
        if not self.total :
            total = sum(item.get_totale_price() for item in self.order.orderproducts_set.all())
            self.total = total
        super().save(*agrs, **kwargs)


class CommandProducts(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price_at_purchase
    
    def __str__(self) -> str:
        return f'{self.product} quantitée commandé : {self.quantity}'