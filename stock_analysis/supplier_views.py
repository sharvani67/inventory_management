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
    suppliers = Supplier.objects.all()
    return render(request, "suppliers/supplier_list.html", {"suppliers": suppliers})
