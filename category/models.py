from django.db import models
from django.db import models
from django.urls import reverse
# Create your models here.
class category(models.Model):
    category_name= models.CharField(max_length=50,unique=True)
    cat_slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=300,null=True)
    c_offer=models.BooleanField(default=False)
    category_image=models.ImageField(upload_to='media',blank=True,null=True)
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'

    def get_url(self):
        return reverse('products_by_category',args=[self.cat_slug])

    def __str__(self):
        return self.category_name