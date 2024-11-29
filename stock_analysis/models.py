

# Create your models here.
from django.db import models
from django.utils.timezone import now
from decimal import Decimal

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
        # Convert 0.8 to Decimal
        cost_price_per_unit = self.product.price_per_unit * Decimal('0.8')

        # Calculate profit using Decimal for accuracy
        profit_per_unit = self.product.price_per_unit - cost_price_per_unit
        self.profit = profit_per_unit * self.quantity_sold

        super().save(*args, **kwargs)


# Model for Customer information
class Customer(models.Model):
    name = models.CharField(max_length=100)  # Customer name
    contact = models.CharField(max_length=15, blank=True, null=True)  # Phone or email
    address = models.TextField(blank=True, null=True)  # Address

    def __str__(self):
        return self.name
    

# Supplier Model
class Supplier(models.Model):
    name = models.CharField(max_length=100)  # Supplier name
    contact = models.CharField(max_length=15, blank=True, null=True)  # Contact details
    address = models.TextField(blank=True, null=True)  # Address
    company = models.CharField(max_length=100, blank=True, null=True)  # Company name

    def __str__(self):
        return self.name

# SupplierProduct Model
class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)  # Link to Supplier
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product
    quantity_supplied = models.IntegerField()  # Quantity supplied
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)  # Cost price per unit
    supplied_date = models.DateField(auto_now_add=True)  # Date of supply

    def __str__(self):
        return f"{self.product.name} supplied by {self.supplier.name}"
