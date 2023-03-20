from django.db import models
from category.models import category
from django.urls import reverse
# Create your models here.


class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    prod_slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=500,blank=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to='media')
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now=True)
    modified_date=models.DateTimeField(auto_now=True)
    p_offer=models.FloatField(blank=True,default=0)
    cat_offer=models.FloatField(blank=True, default=0)
                                

    def get_url(self):
        return reverse('product_detail',args=[self.category.cat_slug,self.prod_slug])
    def __str__(self):
        return self.product_name