from datetime import datetime, timedelta
from .models import SupplierProduct,Sale
from django.shortcuts import render

# Manager Dashboard

# Manager Dashboard
def manager_dashboard(request):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Low stock warning logic (Low stock products from stock analysis)
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


from django.shortcuts import render
from .models import SupplierProduct, Sale
from django.db.models import Sum


def stock_analysis_list(request):
    # Get all the SupplierProduct instances
    supplier_products = SupplierProduct.objects.all()

    stock_analysis_data = []
    
    for supplier_product in supplier_products:
        # Get total quantity supplied for the product (stock_quantity)
        quantity_supplied = supplier_product.stock_quantity

        # Get total quantity sold for the product
        quantity_sold = Sale.objects.filter(supplier_product=supplier_product).aggregate(Sum('quantity_sold'))['quantity_sold__sum'] or 0

        # Calculate remaining stock
        remaining_stock = quantity_supplied - quantity_sold

        # Create a dictionary for the stock analysis data
        stock_analysis_data.append({
            'product_name': supplier_product.name,  # Use 'name' field from SupplierProduct
            'quantity_supplied': quantity_supplied,
            'quantity_sold': quantity_sold,
            'remaining_stock': remaining_stock,
        })
    
    return render(request, 'stock_analysis_list.html', {'stock_analysis_data': stock_analysis_data})




# Index view
def index(request):
    return render(request, 'index.html')

from .models import Sale

def customer_list(request):
    # Fetch all sales records, you can filter or order them if needed
    sales = Sale.objects.all()
    
    return render(request, 'customers_list.html', {'sales': sales})

# home view
def home(request):
    return render(request, 'home.html')