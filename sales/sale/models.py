from customers.models import Customer
from profiles.models import Profile
from products.models import Product
from django.db import models
from django.utils import timezone

class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created = models.DateField(blank=True)
    
    def __str__(self):
        return f"id : {self.id} , product : {self.product.name} , quantity : {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)


class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateField(blank=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Sales of amount Rs. {self.total_price}"
    
    def save(self, *args, **kwargs):
        if self.transaction_id=="":
            self.transaction_id = ''
        if self.created is None:
            self.created = timezone.now()
        return super().save(*args, **kwargs)
    
    def get_positions(self):
        return self.positions.all()


class CSV(models.Model):
    file_name = models.FileField(upload_to = 'csvs')
    activated = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.file_name)