from django.contrib import admin
from .models import ProductSubCategory, ProductCategory, ProductSubCategoryDetail, Settings, User, Basket, TempBask

admin.site.register([ProductSubCategory, ProductCategory, ProductSubCategoryDetail, Settings, User])
admin.site.register([Basket, TempBask])



