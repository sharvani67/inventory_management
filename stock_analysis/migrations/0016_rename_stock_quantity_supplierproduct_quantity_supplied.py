# Generated by Django 5.1.3 on 2024-12-10 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_analysis', '0015_remove_sale_product_remove_supplierproduct_product_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplierproduct',
            old_name='stock_quantity',
            new_name='quantity_supplied',
        ),
    ]
