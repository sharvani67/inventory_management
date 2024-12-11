from django.urls import path
from . import sales_views,supplier_views,product_views,registration_views,views,price_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

urlpatterns = [
    path("index/",login_required(views.index),name="index"),
    path('customer-list/',login_required(views.customer_list), name='customer_list'),
    path('register/', registration_views.register, name='register'),
    path('login/', registration_views.login_view, name='login'),
    path('logout/', registration_views.logout_view, name='logout'),
    
    # Sales
    path("add-sale/", login_required(sales_views.add_sale), name="add_sale"),
    path("sales/", login_required(sales_views.sales_list), name="sales_list"),
    path("sales/update/<int:sale_id>/",login_required(sales_views.update_sale), name="update_sale"),
    path('sales/delete/<int:sale_id>/',login_required(sales_views.delete_sale), name='delete_sale'),
    
    # Dashboards
    path("manager-dashboard/", login_required(views.manager_dashboard), name="manager_dashboard"),
    path("owner-dashboard/", login_required(views.owner_dashboard), name="owner_dashboard"),
    
    # Supplier Products
    path("add-supplier-product/", login_required(product_views.add_supplier_product), name="add_supplier_product"),
    path("supplier-products/", login_required(product_views.supplier_product_list), name="supplier_product_list"),
    path('update-product/<int:product_id>/', login_required(product_views.update_supplier_product), name='update_supplier_product'),
    path('delete-supplier-product/<int:product_id>/', login_required(product_views.delete_supplier_product), name='delete_supplier_product'),
    
    # Suppliers
    path("add-supplier/", login_required(supplier_views.add_supplier), name="add_supplier"),
    path("suppliers/", login_required(supplier_views.supplier_list), name="supplier_list"),
    path('supplier/update/<int:pk>/', login_required(supplier_views.update_supplier), name='update_supplier'),
    path('supplier/delete/<int:pk>/', login_required(supplier_views.delete_supplier), name='delete_supplier'),


    #price 
    path('add-selling-price/', login_required(price_views.add_selling_price), name='add_selling_price'),
    path('selling-price-list/', login_required(price_views.selling_price_list), name='selling_price_list'),
    path('selling_price/update/<int:selling_price_id>/', login_required(price_views.update_selling_price), name='update_selling_price'),
    path('selling_price/delete/<int:selling_price_id>/', login_required(price_views.delete_selling_price), name='delete_selling_price'),


    path('stock-analysis/',login_required(views.stock_analysis_list), name='stock_analysis_list'),
    path('home/',login_required(views.home), name='home'),

    path('', lambda request: redirect('login/')),  # Redirect to the login page

]
