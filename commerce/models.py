from django.db import models

# Create your models here.
class Seller(models.Model):
  name = models.CharField(max_length=100)
  phoneNumber = models.CharField(max_length=20)


class Item(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField()
  image = models.ImageField(upload_to='images/')
  price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='items')
  created_at = models.DateField(auto_now=True)
  