from django.contrib import admin
from .models import category
# Register your models here.

class categoryAdmin(admin.ModelAdmin):
 
      prepopulated_fields={'cat_slug':('category_name',)}
      list_display=('category_name','cat_slug')


admin.site.register(category,categoryAdmin)