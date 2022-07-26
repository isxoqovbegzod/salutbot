from .models import Settings, User, ProductSubCategory, User, ProductCategory, ProductSubCategoryDetail


def models_method():
    btn_category = ProductSubCategory.objects.all()
    print(btn_category)


def choice_sub_categoty(message):
    model = ProductSubCategoryDetail.objects.all()




