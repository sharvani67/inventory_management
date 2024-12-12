from datetime import datetime, timedelta
from .models import SupplierProduct,Sale
from django.shortcuts import render

# Manager Dashboard

from django.shortcuts import render
from django.db.models import Sum, Q
from datetime import datetime, timedelta
from .models import Sale, SupplierProduct

def manager_dashboard(request):
    # Get the current date and calculate date ranges
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())  # Start of the week (Monday)
    month_start = today.replace(day=1)  # Start of the month

    # Daily Sales Analysis
    daily_sales = Sale.objects.filter(sale_date__date=today).aggregate(
        total_sales=Sum('quantity_sold'), total_revenue=Sum('total_price')
    )

    # Weekly Sales Analysis
    weekly_sales = Sale.objects.filter(sale_date__date__gte=week_start).aggregate(
        total_sales=Sum('quantity_sold'), total_revenue=Sum('total_price')
    )

    # Monthly Sales Analysis
    monthly_sales = Sale.objects.filter(sale_date__date__gte=month_start).aggregate(
        total_sales=Sum('quantity_sold'), total_revenue=Sum('total_price')
    )

    # Low Stock Products
    low_stock_threshold = 10  # Example threshold for low stock
    low_stock_products = []

    for product in SupplierProduct.objects.all():
        # Calculate remaining stock
        quantity_supplied = product.stock_quantity
        quantity_sold = Sale.objects.filter(supplier_product=product).aggregate(
            total_sold=Sum('quantity_sold')
        )['total_sold'] or 0
        remaining_stock = quantity_supplied - quantity_sold

        if remaining_stock < low_stock_threshold:
            low_stock_products.append({
                'product_name': product.name,
                'remaining_stock': remaining_stock,
            })

    context = {
        'daily_sales': daily_sales,
        'weekly_sales': weekly_sales,
        'monthly_sales': monthly_sales,
        'low_stock_products': low_stock_products,
    }

    return render(request, 'manager_dashboard.html', context)




from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime
from .models import Sale

def owner_dashboard(request):
    # Get the current date
    today = datetime.now()

    # Monthly Analysis
    month_start = today.replace(day=1)
    monthly_data = Sale.objects.filter(sale_date__date__gte=month_start).aggregate(
        total_revenue=Sum('total_price'),
        total_profit=Sum('profit')
    )
    monthly_revenue = monthly_data['total_revenue'] or 0
    monthly_profit = monthly_data['total_profit'] or 0
    monthly_loss = max(0, monthly_revenue - monthly_profit)  # Calculate loss if any

    # Yearly Analysis
    year_start = today.replace(month=1, day=1)
    yearly_data = Sale.objects.filter(sale_date__date__gte=year_start).aggregate(
        total_revenue=Sum('total_price'),
        total_profit=Sum('profit')
    )
    yearly_revenue = yearly_data['total_revenue'] or 0
    yearly_profit = yearly_data['total_profit'] or 0
    yearly_loss = max(0, yearly_revenue - yearly_profit)  # Calculate loss if any

    context = {
        'monthly_revenue': monthly_revenue,
        'monthly_profit': monthly_profit,
        'monthly_loss': monthly_loss,
        'yearly_revenue': yearly_revenue,
        'yearly_profit': yearly_profit,
        'yearly_loss': yearly_loss,
    }

    return render(request, 'owner_dashboard.html', context)



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
    sales = Sale.objects.all().order_by("-sale_date")
    
    return render(request, 'customers_list.html', {'sales': sales})

# home view
def home(request):
    return render(request, 'home.html')