from django.db import models

class Product(models.Model) :
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to = 'products', default='no_picture.png')
    price = models.FloatField(help_text='in Rs.')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.created.strftime('%d/%m/%Y')}"

    def __repr__(self):
        return f"{self.name} - {self.created.strftime('%d/%m/%Y')}"