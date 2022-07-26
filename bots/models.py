from django.db import models

class User(models.Model):
    chat_id = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    locations = models.CharField(max_length=300, null=True, blank=True)
    choice_price_type = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.category_name


class ProductSubCategoryDetail(models.Model):
    connect_product_categoty = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    sub_categoty_name = models.CharField(max_length=200, null=True, blank=True)
    sub_category_image = models.ImageField(upload_to='image/sub_cat_image/', null=True, blank=True)
    product_price = models.CharField(max_length=255, null=True, blank=True)
    product_qty = models.IntegerField(default=1, null=True, blank=True)
    deskripsiyon = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.sub_categoty_name


class ProductSubCategory(models.Model):
    category_image = models.ImageField(upload_to='image/cat_image')
    product_sub_cat = models.ManyToManyField(ProductSubCategoryDetail)

    # def __str__(self) -> str:
    #     return [i.sub_categoty_name for i in self.product_sub_cat]


class Settings(models.Model):
    toll_price = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.toll_price
