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
    # Annotate SupplierProduct with quantities sold
    supplier_products = SupplierProduct.objects.annotate(
        quantity_sold=Sum('sale__quantity_sold')
    ).values(
        'name',  # Product name
        'stock_quantity',  # Remaining stock
        'quantity_sold',  # Quantity sold (calculated)
        'category',  # Optional: Include category
        'supplier__name',  # Supplier name
        
    )
    
    # Calculate the quantity supplied (quantity_sold + remaining stock)
    stock_analysis = [
        {
            "name": sp["name"],
            "category": sp["category"],
            "supplier": sp["supplier__name"],
            "quantity_supplied": sp["stock_quantity"] or 0,
            "quantity_sold": sp["quantity_sold"] or 0,
            "remaining_stock": sp["stock_quantity"] - (sp["quantity_sold"] or 0),
            
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