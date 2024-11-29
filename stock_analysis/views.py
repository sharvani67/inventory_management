
from django.shortcuts import render, redirect
from .models import Product, Sale
from django.utils.timezone import now

# View for adding a product
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        stock_quantity = request.POST.get("stock_quantity")
        price_per_unit = request.POST.get("price_per_unit")

        # Save product to the database
        Product.objects.create(
            name=name,
            category=category,
            stock_quantity=stock_quantity,
            price_per_unit=price_per_unit
        )
        return redirect("product_list")  # Redirect to product list after adding
    return render(request, "inventory/add_product.html")

# View for listing products
def product_list(request):
    products = Product.objects.all()
    return render(request, "inventory/product_list.html", {"products": products})

# View for adding a sale
def add_sale(request):
    products = Product.objects.all()
    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity_sold = int(request.POST.get("quantity_sold"))

        product = Product.objects.get(id=product_id)
        if product.stock_quantity >= quantity_sold:
            total_price = quantity_sold * product.price_per_unit

            # Save sale to the database
            Sale.objects.create(
                product=product,
                quantity_sold=quantity_sold,
                total_price=total_price,
                sale_date=now()
            )

            # Update product stock
            product.stock_quantity -= quantity_sold
            product.save()

            return redirect("sales_list")  # Redirect to sales list after adding
        else:
            return render(request, "inventory/add_sale.html", {"products": products, "error": "Not enough stock!"})
    return render(request, "inventory/add_sale.html", {"products": products})

# View for listing sales
def sales_list(request):
    sales = Sale.objects.all()
    return render(request, "inventory/sales_list.html", {"sales": sales})

from django.db.models import Sum
from datetime import datetime, timedelta

# View for Manager Analytics
def manager_dashboard(request):
    # Get today's date
    today = datetime.now().date()

    # Calculate date ranges
    start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week
    start_of_month = today.replace(day=1)  # First day of the current month

    # Aggregated stock data
    low_stock_products = Product.objects.filter(stock_quantity__lt=10)  # Low stock warning (<10 units)

    # Sales data
    daily_sales = Sale.objects.filter(sale_date__date=today).aggregate(total=Sum('total_price'))['total'] or 0
    weekly_sales = Sale.objects.filter(sale_date__date__gte=start_of_week).aggregate(total=Sum('total_price'))['total'] or 0
    monthly_sales = Sale.objects.filter(sale_date__date__gte=start_of_month).aggregate(total=Sum('total_price'))['total'] or 0

    # Pass data to the template
    context = {
        "low_stock_products": low_stock_products,
        "daily_sales": daily_sales,
        "weekly_sales": weekly_sales,
        "monthly_sales": monthly_sales,
    }
    return render(request, "inventory/manager_dashboard.html", context)

from django.db.models import Sum
from datetime import datetime

# View for Owner Dashboard
def owner_dashboard(request):
    today = datetime.now().date()

    # Monthly analysis
    start_of_month = today.replace(day=1)
    monthly_revenue = Sale.objects.filter(sale_date__date__gte=start_of_month).aggregate(total=Sum('total_price'))['total'] or 0
    monthly_profit = Sale.objects.filter(sale_date__date__gte=start_of_month).aggregate(total=Sum('profit'))['total'] or 0

    # Yearly analysis
    start_of_year = today.replace(month=1, day=1)
    yearly_revenue = Sale.objects.filter(sale_date__date__gte=start_of_year).aggregate(total=Sum('total_price'))['total'] or 0
    yearly_profit = Sale.objects.filter(sale_date__date__gte=start_of_year).aggregate(total=Sum('profit'))['total'] or 0

    context = {
        "monthly_revenue": monthly_revenue,
        "monthly_profit": monthly_profit,
        "yearly_revenue": yearly_revenue,
        "yearly_profit": yearly_profit,
    }
    return render(request, "inventory/owner_dashboard.html", context)


