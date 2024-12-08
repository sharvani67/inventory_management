from django.urls import path
from . import sales_views,supplier_views,product_views,registration_views,views

urlpatterns = [
    path("index/",views.index,name="index"),
    path('customer-list/', views.customer_list, name='customer_list'),
    path('register/', registration_views.register, name='register'),
    path('login/', registration_views.login_view, name='login'),
    path('logout/', registration_views.logout_view, name='logout'),
    
    # Sales
    path("add-sale/", sales_views.add_sale, name="add_sale"),
    path("sales/", sales_views.sales_list, name="sales_list"),
    
    # Dashboards
    path("manager-dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("owner-dashboard/", views.owner_dashboard, name="owner_dashboard"),
    
    # Supplier Products
    path("add-supplier-product/", product_views.add_supplier_product, name="add_supplier_product"),
    path("supplier-products/", product_views.supplier_product_list, name="supplier_product_list"),
    
    # Suppliers
    path("add-supplier/", supplier_views.add_supplier, name="add_supplier"),
    path("suppliers/", supplier_views.supplier_list, name="supplier_list"),

    path('stock-analysis/', views.stock_analysis_list, name='stock_analysis_list'),
    path('home/', views.home, name='home'),

]
