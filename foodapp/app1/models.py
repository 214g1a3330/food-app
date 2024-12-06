from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Fooditem(models.Model):
    
    itempic = models.ImageField(upload_to="images")
    itemname = models.CharField(max_length=100)
    price = models.FloatField()
    itemtype = models.CharField(max_length=100)
    rating = models.FloatField()
    availability = models.BooleanField()
    
    def __str__(self) -> str:
        return self.itemname
    
    
    
class Cart(models.Model):
    
    item = models.ForeignKey("Fooditem", on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.item.itemname
    
    
    
class Order(models.Model):
    
    usern = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    items = models.ForeignKey("Cart", on_delete=models.CASCADE)
    addr = models.TextField()
    phno = models.CharField(max_length=10)
    
    def __str__(self) -> str:
        return str(self.id)