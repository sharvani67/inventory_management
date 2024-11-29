

# Create your models here.
from django.db import models
from django.utils.timezone import now

# Model for Product details
class Product(models.Model):
    name = models.CharField(max_length=100)  # Product name (e.g., Eggs)
    category = models.CharField(max_length=50, blank=True, null=True)  # Product category (e.g., Size)
    stock_quantity = models.IntegerField(default=0)  # Current stock quantity
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for updates

    def __str__(self):
        return self.name

# Model for Sales transactions
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Profit for this sale
    sale_date = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        # Calculate profit as revenue minus cost (assuming cost is 80% of price_per_unit)
        cost_price = self.product.price_per_unit * 0.8
        self.profit = (self.product.price_per_unit - cost_price) * self.quantity_sold
        super().save(*args, **kwargs)


# Model for Customer information
class Customer(models.Model):
    name = models.CharField(max_length=100)  # Customer name
    contact = models.CharField(max_length=15, blank=True, null=True)  # Contact number
    email = models.EmailField(blank=True, null=True)  # Email address

    def __str__(self):
        return self.name
    


