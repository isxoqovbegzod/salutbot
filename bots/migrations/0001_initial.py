# Generated by Django 4.0.6 on 2022-07-25 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toll_price', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('locations', models.CharField(max_length=300)),
                ('choice_price_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSubCategoryDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_categoty_name', models.CharField(max_length=200)),
                ('sub_category_image', models.ImageField(upload_to='image/sub_cat_image/')),
                ('product_price', models.FloatField()),
                ('product_qty', models.IntegerField(default=1)),
                ('deskripsiyon', models.CharField(max_length=255)),
                ('connect_product_categoty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bots.productcategory')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_image', models.ImageField(upload_to='image/cat_image')),
                ('product_sub_cat', models.ManyToManyField(to='bots.productsubcategorydetail')),
            ],
        ),
    ]
