from .models import Supplier
from django.shortcuts import render, redirect

# View to add a supplier
def add_supplier(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        address = request.POST.get("address")
        company = request.POST.get("company")
        date = request.POST.get("date") or None

        # Save the supplier
        Supplier.objects.create(
            name=name,
            contact=contact,
            email=email,
            address=address,
            company=company,
            partnership_date=date
        )
        return redirect("supplier_list")  # Redirect to the supplier list

    return render(request, "suppliers/add_supplier.html")

# View to list all suppliers
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by("-partnership_date") 
    return render(request, "suppliers/supplier_list.html", {"suppliers": suppliers})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Supplier

from django.shortcuts import render, get_object_or_404, redirect
from .models import Supplier

def update_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.name = request.POST.get('name')
        supplier.contact = request.POST.get('contact')
        supplier.email = request.POST.get('email')
        supplier.address = request.POST.get('address')
        supplier.company = request.POST.get('company')
        supplier.partnership_date = request.POST.get('date')
        supplier.save()
        return redirect('supplier_list')  # Replace 'supplier_list' with the name of your supplier list view
    return render(request, 'suppliers/update_supplier.html', {'supplier': supplier})

def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('supplier_list')  # Replace 'supplier_list' with the name of your supplier list view
