from django.shortcuts import render, redirect,get_object_or_404
from .models import SupplierProduct,Sale
from django.db.models import Sum
from django.utils.timezone import now

def add_sale(request):
    # Fetch all supplier products
    supplier_products = SupplierProduct.objects.all()

    # Calculate remaining stock for each product
    for product in supplier_products:
        # Get total quantity supplied and total quantity sold for the product
        total_supplied = product.stock_quantity
        total_sold = Sale.objects.filter(supplier_product=product).aggregate(Sum('quantity_sold'))['quantity_sold__sum'] or 0
        product.remaining_stock = total_supplied - total_sold

    if request.method == "POST":
        customer_name=request.POST.get("customer_name")
        customer_mobile=request.POST.get("customer_mobile")
        supplier_product_id = request.POST.get("supplier_product")
        quantity_sold = int(request.POST.get("quantity_sold"))
        our_selling_price_per_unit = float(request.POST.get("our_selling_price_per_unit"))

        supplier_product = get_object_or_404(SupplierProduct, id=supplier_product_id)

        # Calculate available stock for the selected product
        total_supplied = supplier_product.stock_quantity
        total_sold = Sale.objects.filter(supplier_product=supplier_product).aggregate(Sum('quantity_sold'))['quantity_sold__sum'] or 0
        remaining_stock = total_supplied - total_sold

        # Check if the quantity sold exceeds the available stock
        if quantity_sold > remaining_stock:
            # Return a warning message if not enough stock is available
            error_message = f"Not enough stock! Only {remaining_stock} items available."
            return render(request, "sales/add_sale.html", {"supplier_products": supplier_products, "error_message": error_message})

        # Get supplier's selling price per unit
        supplier_selling_price = float(supplier_product.selling_price_per_unit)

        # Calculate total price and profit
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

        # After the sale, update the remaining stock of the product
        supplier_product.remaining_stock = remaining_stock - quantity_sold
        supplier_product.save()

        # Redirect to sales list after saving the sale
        return redirect("sales_list")

    return render(request, "sales/add_sale.html", {"supplier_products": supplier_products, "error_message": ""})



# List all sales
def sales_list(request):
    sales = Sale.objects.select_related("supplier_product__supplier")
    return render(request, "sales/sales_list.html", {"sales": sales})

