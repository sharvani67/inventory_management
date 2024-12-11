from django.shortcuts import render, redirect, get_object_or_404
from .models import SupplierProduct, Sale, SellingPrice
from django.db.models import Sum
from django.utils.timezone import now
from decimal import Decimal

def add_sale(request):
    # Fetch all supplier products
    supplier_products = SupplierProduct.objects.all(
        
    )

    # Prepare a dictionary of selling prices for each product
    selling_prices = {
        product.id: product.selling_price_per_unit
        for product in supplier_products
    }

    # Calculate remaining stock for each product
    for product in supplier_products:
        total_supplied = product.stock_quantity
        total_sold = Sale.objects.filter(supplier_product=product).aggregate(Sum('quantity_sold'))['quantity_sold__sum'] or 0
        product.remaining_stock = total_supplied - total_sold

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        customer_mobile = request.POST.get("customer_mobile")
        supplier_product_id = request.POST.get("supplier_product")
        quantity_sold = int(request.POST.get("quantity_sold"))
        our_selling_price_per_unit = float(request.POST.get("our_selling_price_per_unit"))

        supplier_product = get_object_or_404(SupplierProduct, id=supplier_product_id)

        # Get the selling price from the SellingPrice model, not SupplierProduct directly
        selling_price_record = SellingPrice.objects.filter(supplier_product=supplier_product).first()
        if selling_price_record:
            our_selling_price_per_unit = selling_price_record.our_selling_price_per_unit
        else:
            # If no selling price is found, use the default selling price
            our_selling_price_per_unit = supplier_product.selling_price_per_unit

        # Calculate available stock for the selected product
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

        # Get supplier's selling price per unit
        supplier_selling_price = Decimal(supplier_product.selling_price_per_unit)

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

from django.shortcuts import render, get_object_or_404, redirect
from .models import Sale  # Adjust based on your app name

def update_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    supplier_products = SupplierProduct.objects.all()

    if request.method == "POST":
        # Get form data
        sale.customer_name = request.POST["customer_name"]
        sale.customer_mobile = request.POST["customer_mobile"]
        product_id = request.POST["supplier_product"]
        sale.supplier_product = get_object_or_404(SupplierProduct, id=product_id)
        sale.quantity_sold = int(request.POST["quantity_sold"])
        sale.our_selling_price_per_unit = float(request.POST["our_selling_price_per_unit"])

        # Update total price
        sale.total_price = sale.quantity_sold * sale.our_selling_price_per_unit

        # Save the sale
        sale.save()
        return redirect("sales_list")  # Redirect to the sales list after updating

    return render(request, "sales/update_sale.html", {"sale": sale, "supplier_products": supplier_products})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Sale

def delete_sale(request, sale_id):
    """
    View to delete a sale record directly.
    """
    sale = get_object_or_404(Sale, id=sale_id)
    sale.delete()
    messages.success(request, "Sale record deleted successfully!")
    return redirect('sales_list')

