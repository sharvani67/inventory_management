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

# sale model 
class Sale(models.Model):
    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE, null=True, blank=True)
    quantity_sold = models.IntegerField()
    our_selling_price_per_unit = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    profit = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    sale_date = models.DateTimeField(default=now)
    customer_name=models.CharField(max_length=100,default="Unknown Customers", blank=True, null=True)
    customer_mobile=models.CharField(max_length=15, blank=True, null=True)
    
    from decimal import Decimal

def save(self, *args, **kwargs):
    # Convert our_selling_price_per_unit to Decimal
    our_selling_price_per_unit = Decimal(self.our_selling_price_per_unit)

    # Calculate total price
    self.total_price = our_selling_price_per_unit * self.quantity_sold

    # Calculate profit
    cost_price = self.supplier_product.selling_price_per_unit
    profit_per_unit = our_selling_price_per_unit - cost_price
    self.profit = profit_per_unit * self.quantity_sold

    # Do NOT modify stock_quantity in SupplierProduct
    super().save(*args, **kwargs)

    

