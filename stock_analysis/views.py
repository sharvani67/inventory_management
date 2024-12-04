from datetime import datetime, timedelta
from .models import SupplierProduct,Sale
from django.shortcuts import render

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

    return render(request, "manager_dashboard.html", {
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

    return render(request, "owner_dashboard.html", {
        "monthly_revenue": monthly_revenue,
        "monthly_profit": monthly_profit,
        "yearly_revenue": yearly_revenue,
        "yearly_profit": yearly_profit,
    })



from django.db.models import Sum

def stock_analysis_list(request):
    # Aggregate data by product name
    supplier_products = SupplierProduct.objects.values(
        'name',  # Group by product name
        'category'  # Optional: Include category
    ).annotate(
        total_quantity_supplied=Sum('stock_quantity'),  # Sum stock for the product across suppliers
        total_quantity_sold=Sum('sale__quantity_sold'),  # Sum sold quantities for the product
    )
    
    # Prepare stock analysis data for rendering
    stock_analysis = [
        {
            "name": sp["name"],
            "category": sp["category"],
            "quantity_supplied": sp["total_quantity_supplied"] or 0,  # Total quantity supplied for the product
            "quantity_sold": sp["total_quantity_sold"] or 0,  # Total quantity sold for the product
            "remaining_stock": (sp["total_quantity_supplied"] or 0) - (sp["total_quantity_sold"] or 0),
        }
        for sp in supplier_products
    ]

    return render(request, "stock_analysis_list.html", {"stock_analysis": stock_analysis})


# Index view
def index(request):
    return render(request, 'index.html')

from .models import Sale

def customer_list(request):
    # Fetch all sales records, you can filter or order them if needed
    sales = Sale.objects.all()
    
    return render(request, 'customers_list.html', {'sales': sales})