from django.db import models

# Create your models here.


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    product_category = models.CharField(max_length=255)
    product_category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    stocks = models.IntegerField(null=True)
    product_cost = models.IntegerField(null=True)
    product_description = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    