

from django.db import models
from django.utils.timezone import now
from decimal import Decimal


# Supplier Model
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    partnership_date = models.DateField(default=now)  # Default to current date

    def __str__(self):
        return self.name


# SupplierProduct Model
class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)  # Link to Supplier
    name = models.CharField(max_length=100, default="Unknown Product")  # Default name
    category = models.CharField(max_length=50, blank=True, null=True)  # Product category
    selling_price_per_unit=models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)  # Current stock quantity
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)  # Cost price per unit
    supplied_date = models.DateField(auto_now_add=True)  # Date of supply

    def __str__(self):
        return f"{self.name} from {self.supplier.name}"


from decimal import Decimal

class Sale(models.Model):
    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE, null=True, blank=True)
    quantity_sold = models.IntegerField()
    our_selling_price_per_unit = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    profit = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    sale_date = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.our_selling_price_per_unit * self.quantity_sold

        # Get selling price per unit from SupplierProduct
        supplier_selling_price = float(self.supplier_product.selling_price_per_unit)

        # Calculate profit per unit and total profit
        profit_per_unit = self.our_selling_price_per_unit - supplier_selling_price
        self.profit = profit_per_unit * self.quantity_sold

        # Check stock availability
        if self.quantity_sold > self.supplier_product.stock_quantity:
            raise ValueError("Not enough stock to complete the sale.")
        self.supplier_product.stock_quantity -= self.quantity_sold
        self.supplier_product.save()

        super().save(*args, **kwargs)

# Model for Customer information
class Customer(models.Model):
    name = models.CharField(max_length=100)  # Customer name
    contact = models.CharField(max_length=15, blank=True, null=True)  # Phone or email
    address = models.TextField(blank=True, null=True)  # Address

    def __str__(self):
        return self.name
    

