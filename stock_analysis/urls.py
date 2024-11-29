from django.urls import path
from . import views

urlpatterns = [
    path("add-product/", views.add_product, name="add_product"),
    path("products/", views.product_list, name="product_list"),
    path("add-sale/", views.add_sale, name="add_sale"),
    path("sales/", views.sales_list, name="sales_list"),
    path("manager-dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("owner-dashboard/", views.owner_dashboard, name="owner_dashboard"),


]
