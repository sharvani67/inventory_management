from django.shortcuts import render, redirect, get_object_or_404
from .models import SupplierProduct, Supplier

# Add or update product supplied by a supplier
def add_supplier_product(request):
    suppliers = Supplier.objects.all()
    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        product_name = request.POST.get("product_name")
        selling_price_per_unit = request.POST.get("price_per_unit")
        category = request.POST.get("category")
        cost_price = request.POST.get("cost_price")
        quantity_supplied = int(request.POST.get("quantity_supplied"))

        supplier = get_object_or_404(Supplier, id=supplier_id)

        # Check if the product already exists for the supplier
        supplier_product, created = SupplierProduct.objects.get_or_create(
            supplier=supplier,
            name=product_name,
            defaults={
                "category": category,
                "selling_price_per_unit": selling_price_per_unit,
                "cost_price": cost_price,
                "stock_quantity": quantity_supplied,
            }
        )

        if not created:
            # Update stock if the product already exists
            supplier_product.stock_quantity += quantity_supplied
            supplier_product.selling_price_per_unit = selling_price_per_unit
            supplier_product.cost_price = cost_price
            supplier_product.save()

        return redirect("supplier_product_list")  # Redirect to supplier product list

    return render(request, "products/add_supplier_product.html", {"suppliers": suppliers})



# List all products supplied by suppliers
def supplier_product_list(request):
    supplier_products = SupplierProduct.objects.select_related("supplier")
    return render(request, "products/supplier_product_list.html", {"supplier_products": supplier_products})
