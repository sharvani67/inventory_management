# views.py
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SupplierProduct, SellingPrice
from django.utils import timezone

def add_selling_price(request):
     # Fetch all supplier products
    supplier_products = SupplierProduct.objects.all()

    
    if request.method == 'POST':
        supplier_product_id = request.POST.get('supplier_product')
        our_selling_price_per_unit = request.POST.get('our_selling_price_per_unit')

        if not supplier_product_id or not our_selling_price_per_unit:
            messages.error(request, "All fields are required.")
            return redirect('add_selling_price')  # Or render the form with errors

        try:
            supplier_product = SupplierProduct.objects.get(id=supplier_product_id)
            selling_price = SellingPrice(
                supplier_product=supplier_product,
                our_selling_price_per_unit=our_selling_price_per_unit,
                date_added=timezone.now()  # Set current date and time
            )
            selling_price.save()
            messages.success(request, "Selling price added successfully!")
            return redirect('selling_price_list')  # Redirect to a success page or the same form
        except SupplierProduct.DoesNotExist:
            messages.error(request, "Invalid product selected.")
            return redirect('add_selling_price')

    else:
        # Initial empty form
        supplier_products = SupplierProduct.objects.all()
        return render(request, 'prices/add_selling_price.html', {'supplier_products': supplier_products})


from django.shortcuts import render
from .models import SellingPrice

def selling_price_list(request):
    # Fetch all selling prices
    selling_prices = SellingPrice.objects.select_related('supplier_product', 'supplier_product__supplier').all()
    
    # Pass the selling prices to the template
    return render(request, 'prices/selling_price_list.html', {
        'selling_prices': selling_prices
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import SellingPrice, SupplierProduct

def update_selling_price(request, selling_price_id):
    """
    View to update an existing selling price.
    """
    selling_price = get_object_or_404(SellingPrice, id=selling_price_id)
    supplier_products = SupplierProduct.objects.all()

    if request.method == 'POST':
        supplier_product_id = request.POST.get('supplier_product')
        our_selling_price_per_unit = request.POST.get('our_selling_price_per_unit')

        if supplier_product_id and our_selling_price_per_unit:
            selling_price.supplier_product_id = supplier_product_id
            selling_price.our_selling_price_per_unit = our_selling_price_per_unit
            selling_price.save()
            messages.success(request, "Selling price updated successfully!")
            return redirect('selling_price_list')
        else:
            messages.error(request, "Please fill all required fields.")

    return render(request, 'prices/update_selling_price.html', {
        'selling_price': selling_price,
        'supplier_products': supplier_products,
    })


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import SellingPrice

def delete_selling_price(request, selling_price_id):
    """
    View to delete a selling price record.
    """
    selling_price = get_object_or_404(SellingPrice, id=selling_price_id)
    selling_price.delete()
    messages.success(request, "Selling price deleted successfully!")
    return redirect('selling_price_list')
