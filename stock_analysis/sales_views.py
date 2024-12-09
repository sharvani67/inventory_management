from django.shortcuts import render, redirect, get_object_or_404
from .models import SupplierProduct, Sale, SellingPrice
from django.db.models import Sum
from django.utils.timezone import now
from decimal import Decimal

from django.db.models.functions import Lower

def add_sale(request):
    # Fetch distinct product names (case-insensitive)
    supplier_products = SupplierProduct.objects.order_by(Lower('name')).values('name').distinct()

    # Prepare selling prices for each product (optional for autocomplete)
    selling_prices = {
        product['name']: SellingPrice.objects.filter(
            supplier_product__name=product['name']
        ).first().our_selling_price_per_unit
        if SellingPrice.objects.filter(supplier_product__name=product['name']).exists()
        else None
        for product in supplier_products
    }

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        customer_mobile = request.POST.get("customer_mobile")
        product_name = request.POST.get("supplier_product")
        quantity_sold = int(request.POST.get("quantity_sold"))

        # Fetch the first SupplierProduct entry for the selected product name
        supplier_product = SupplierProduct.objects.filter(name=product_name).first()
        if not supplier_product:
            error_message = "Invalid product selected."
            return render(request, "sales/add_sale.html", {
                "supplier_products": supplier_products,
                "selling_prices": selling_prices,
                "error_message": error_message
            })

        # Get the selling price from SellingPrice model
        selling_price_record = SellingPrice.objects.filter(supplier_product=supplier_product).first()
        our_selling_price_per_unit = selling_price_record.our_selling_price_per_unit if selling_price_record else supplier_product.selling_price_per_unit

        # Calculate available stock
        total_supplied = supplier_product.stock_quantity
        total_sold = Sale.objects.filter(supplier_product=supplier_product).aggregate(Sum('quantity_sold'))['quantity_sold__sum'] or 0
        remaining_stock = total_supplied - total_sold

        # Check if the quantity sold exceeds the available stock
        if quantity_sold > remaining_stock:
            error_message = f"Not enough stock! Only {remaining_stock} items available."
            return render(request, "sales/add_sale.html", {
                "supplier_products": supplier_products,
                "selling_prices": selling_prices,
                "error_message": error_message
            })

        # Calculate total price and profit
        supplier_selling_price = Decimal(supplier_product.selling_price_per_unit)
        total_price = quantity_sold * our_selling_price_per_unit
        profit = (our_selling_price_per_unit - supplier_selling_price) * quantity_sold

        # Save the sale record
        Sale.objects.create(
            supplier_product=supplier_product,
            quantity_sold=quantity_sold,
            our_selling_price_per_unit=our_selling_price_per_unit,
            total_price=total_price,
            profit=profit,
            customer_name=customer_name,
            customer_mobile=customer_mobile,
            sale_date=now()
        )

        # Redirect to sales list after saving the sale
        return redirect("sales_list")

    return render(request, "sales/add_sale.html", {
        "supplier_products": supplier_products,
        "selling_prices": selling_prices,
        "error_message": ""
    })





# List all sales
def sales_list(request):
    sales = Sale.objects.select_related("supplier_product__supplier")
    return render(request, "sales/sales_list.html", {"sales": sales})