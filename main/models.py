from django.db import models
from django.utils.text import slugify
import random
import string
import uuid
# Create your models here.


class CustomerDetails(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def generate_owner_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class OwnerDetails(models.Model):
    
    ownerid = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=50)
    mobile = models.CharField(unique=True,max_length=50)
    primaryshopname = models.CharField(max_length=200)
    primaryshopid = models.CharField(max_length=200)
    total_shop_count = models.CharField(max_length=20,null=True)
    
    def save(self, *args, **kwargs):
        if not self.ownerid:
            self.ownerid = generate_owner_id()
        if not self.primaryshopid:
            self.primaryshopid = slugify(self.primaryshopname)
        super().save(*args, **kwargs)
    

class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    shop_id_public = models.CharField(max_length=255,null=True)
    shop_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    shop_logo = models.ImageField(upload_to='shop_resources/logo/',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop_name
    
    def save(self, *args, **kwargs):
        if not self.shop_id_public:
            self.shop_id_public = slugify(self.shop_name)
        super().save(*args, **kwargs)

class Product(models.Model):
    serial_no = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    shopid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255,null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = generate_product_id()
        super().save(*args, **kwargs)
        
    @staticmethod
    def get_next_serial_number(shop_id, category):
        latest_product = Product.objects.filter(shopid=shop_id, category=category).order_by('-serial_no').first()
        if latest_product and latest_product.image:
            serial_number = int(latest_product.image.name.split('-')[-1].split('.')[0])
            return serial_number + 1
        return 1
        
def generate_product_id():
        return uuid.uuid4().hex[:4] + '-' + uuid.uuid4().hex[:4] + '-' + uuid.uuid4().hex[:4]

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order_id} - {self.customer.first_name} {self.customer.last_name}"


# class OrderItem(models.Model):
#     order_item_id = models.AutoField(primary_key=True)
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
    
#     def __str__(self):
#         return f"{self.product.name} ({self.quantity})"

     
    

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=[
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
        ('Cash on Delivery', 'Cash on Delivery')
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    ])

    def __str__(self):
        return f"Payment {self.payment_id} for Order {self.order.order_id}"
  
    
    

