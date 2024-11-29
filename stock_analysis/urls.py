from django.urls import path
from . import views

urlpatterns = [
    path("add-product/", views.add_product, name="add_product"),
    path("products/", views.product_list, name="product_list"),
    path("add-sale/", views.add_sale, name="add_sale"),
    path("sales/", views.sales_list, name="sales_list"),
    path("manager-dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("owner-dashboard/", views.owner_dashboard, name="owner_dashboard"),
    path("add-customer/", views.add_customer, name="add_customer"),
    path("customers/", views.customer_list, name="customer_list"),
    path("add-supplier-product/", views.add_supplier_product, name="add_supplier_product"),
    path("supplier-products/", views.supplier_product_list, name="supplier_product_list"),
    path("add-supplier/", views.add_supplier, name="add_supplier"),
    path("suppliers/", views.supplier_list, name="supplier_list"),


]
