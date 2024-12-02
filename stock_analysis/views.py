

from django.shortcuts import render, redirect, get_object_or_404
from .models import Sale, Supplier, SupplierProduct,Customer
from django.utils.timezone import now
from django.db.models import Sum
from datetime import datetime, timedelta

from .models import Supplier
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

    return render(request, "inventory/add_supplier.html")



# View to list all suppliers
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, "inventory/supplier_list.html", {"suppliers": suppliers})


# Add or update product supplied by a supplier
def add_supplier_product(request):
    suppliers = Supplier.objects.all()
    if request.method == "POST":
        supplier_id = request.POST.get("supplier")
        product_name = request.POST.get("product_name")
        selling_price_per_unit=request.POST.get("price_per_unit")
        category = request.POST.get("category")
        cost_price = request.POST.get("cost_price")
        quantity_supplied = int(request.POST.get("quantity_supplied"))

        supplier = get_object_or_404(Supplier, id=supplier_id)

        # Create or update SupplierProduct
        supplier_product, created = SupplierProduct.objects.get_or_create(
            supplier=supplier,
            name=product_name,
            defaults={
                "category": category,
                "selling_price_per_unit":selling_price_per_unit,
                "cost_price": cost_price,
                "stock_quantity": quantity_supplied,
            },
        )
        if not created:
            supplier_product.stock_quantity += quantity_supplied
            supplier_product.cost_price = cost_price  # Update cost price if provided
            supplier_product.save()

        return redirect("supplier_product_list")  # Redirect to supplier product list

    return render(request, "inventory/add_supplier_product.html", {"suppliers": suppliers})


# List all products supplied by suppliers
def supplier_product_list(request):
    supplier_products = SupplierProduct.objects.select_related("supplier")
    return render(request, "inventory/supplier_product_list.html", {"supplier_products": supplier_products})

from decimal import Decimal

def add_sale(request):
    supplier_products = SupplierProduct.objects.all()
    if request.method == "POST":
        supplier_product_id = request.POST.get("supplier_product")
        quantity_sold = int(request.POST.get("quantity_sold"))
        our_selling_price_per_unit = float(request.POST.get("our_selling_price_per_unit"))

        supplier_product = SupplierProduct.objects.get(id=supplier_product_id)

        if supplier_product.stock_quantity >= quantity_sold:
            # Convert the cost_price to float to ensure both operands are of the same type (float)
            cost_price = float(supplier_product.cost_price)  # Convert Decimal to float

            # Calculate total price and profit
            total_price = quantity_sold * our_selling_price_per_unit
            profit = (our_selling_price_per_unit - cost_price) * quantity_sold

            # Save the sale
            Sale.objects.create(
                supplier_product=supplier_product,
                quantity_sold=quantity_sold,
                our_selling_price_per_unit=our_selling_price_per_unit,
                total_price=total_price,
                profit=profit,
                sale_date=now()
            )

            # Update stock quantity
            supplier_product.stock_quantity -= quantity_sold
            supplier_product.save()

            return redirect("sales_list")  # Redirect to sales list
        else:
            return render(request, "inventory/add_sale.html", {
                "supplier_products": supplier_products,
                "error": "Not enough stock!",
            })

    return render(request, "inventory/add_sale.html", {"supplier_products": supplier_products})


# List all sales
def sales_list(request):
    sales = Sale.objects.select_related("supplier_product__supplier")
    return render(request, "inventory/sales_list.html", {"sales": sales})


# Manager Dashboard
def manager_dashboard(request):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Low stock warning
    low_stock_products = SupplierProduct.objects.filter(stock_quantity__lt=10)

    # Sales data
    daily_sales = Sale.objects.filter(sale_date__date=today).aggregate(total=Sum('total_price'))['total'] or 0
    weekly_sales = Sale.objects.filter(sale_date__date__gte=start_of_week).aggregate(total=Sum('total_price'))['total'] or 0
    monthly_sales = Sale.objects.filter(sale_date__date__gte=start_of_month).aggregate(total=Sum('total_price'))['total'] or 0

    return render(request, "inventory/manager_dashboard.html", {
        "low_stock_products": low_stock_products,
        "daily_sales": daily_sales,
        "weekly_sales": weekly_sales,
        "monthly_sales": monthly_sales,
    })


# Owner Dashboard
def owner_dashboard(request):
    today = datetime.now().date()
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    # Revenue and profit analysis
    monthly_revenue = Sale.objects.filter(sale_date__date__gte=start_of_month).aggregate(total=Sum('total_price'))['total'] or 0
    monthly_profit = Sale.objects.filter(sale_date__date__gte=start_of_month).aggregate(total=Sum('profit'))['total'] or 0
    yearly_revenue = Sale.objects.filter(sale_date__date__gte=start_of_year).aggregate(total=Sum('total_price'))['total'] or 0
    yearly_profit = Sale.objects.filter(sale_date__date__gte=start_of_year).aggregate(total=Sum('profit'))['total'] or 0

    return render(request, "inventory/owner_dashboard.html", {
        "monthly_revenue": monthly_revenue,
        "monthly_profit": monthly_profit,
        "yearly_revenue": yearly_revenue,
        "yearly_profit": yearly_profit,
    })


# View for adding a customer
def add_customer(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        address = request.POST.get("address")

        # Save the customer
        Customer.objects.create(name=name, contact=contact, address=address)
        return redirect("customer_list")  # Redirect to customer list
    return render(request, "inventory/add_customer.html")

# View for listing customers
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "inventory/customer_list.html", {"customers": customers})