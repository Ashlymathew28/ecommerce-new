from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from store.models import Product
from category.models import category
# Create your models here.


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=25)
    coupon_code = models.CharField(max_length=20,unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(
        validators = [MinValueValidator(0),MaxValueValidator(100)]
    )
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.coupon_code
    
class product_offer(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    offer=models.FloatField()
    offer_type = models.CharField(max_length=200,default='Product')
    # start_date=models.DateField()
    # end_date=models.DateField()
    is_active=models.BooleanField(default=True)

class cat_offer(models.Model):
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    offer=models.FloatField()
    offer_type=models.CharField(max_length=100)
    # start_date=models.DateField()
    # end_date=models.DateField()
    is_active=models.BooleanField(default=True)
    
