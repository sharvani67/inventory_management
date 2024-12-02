from django.urls import path
from . import views

urlpatterns = [
    # Sales
    path("add-sale/", views.add_sale, name="add_sale"),
    path("sales/", views.sales_list, name="sales_list"),
    
    # Dashboards
    path("manager-dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("owner-dashboard/", views.owner_dashboard, name="owner_dashboard"),
    
    # Customers
    path("add-customer/", views.add_customer, name="add_customer"),
    path("customers/", views.customer_list, name="customer_list"),
    
    # Supplier Products
    path("add-supplier-product/", views.add_supplier_product, name="add_supplier_product"),
    path("supplier-products/", views.supplier_product_list, name="supplier_product_list"),
    
    # Suppliers
    path("add-supplier/", views.add_supplier, name="add_supplier"),
    path("suppliers/", views.supplier_list, name="supplier_list"),
]
