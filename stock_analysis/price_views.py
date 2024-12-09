# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SupplierProduct, SellingPrice
from django.utils import timezone
from django.db.models.functions import Lower

def add_selling_price(request):
    # Get distinct product names (case-insensitive)
    supplier_products = SupplierProduct.objects.order_by(Lower('name')).values('name').distinct()

    if request.method == 'POST':
        # Fetch the selected product name from the form
        product_name = request.POST.get('supplier_product')
        our_selling_price_per_unit = request.POST.get('our_selling_price_per_unit')

        # Validate input
        if not product_name or not our_selling_price_per_unit:
            messages.error(request, "All fields are required.")
            return redirect('add_selling_price')

        try:
            # Fetch the first SupplierProduct with the selected name
            supplier_product = SupplierProduct.objects.filter(name=product_name).first()

            if not supplier_product:
                messages.error(request, "Invalid product selected.")
                return redirect('add_selling_price')

            # Save the selling price
            selling_price = SellingPrice(
                supplier_product=supplier_product,
                our_selling_price_per_unit=our_selling_price_per_unit,
                date_added=timezone.now()
            )
            selling_price.save()

            messages.success(request, "Selling price added successfully!")
            return redirect('selling_price_list')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add_selling_price')

    return render(request, 'prices/add_selling_price.html', {
        'supplier_products': supplier_products,
    })


from django.shortcuts import render
from .models import SellingPrice

def selling_price_list(request):
    # Fetch all selling prices
    selling_prices = SellingPrice.objects.select_related('supplier_product', 'supplier_product__supplier').all()
    
    # Pass the selling prices to the template
    return render(request, 'prices/selling_price_list.html', {
        'selling_prices': selling_prices
    })