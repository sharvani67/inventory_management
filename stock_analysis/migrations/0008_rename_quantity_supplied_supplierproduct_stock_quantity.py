# Generated by Django 5.1.2 on 2024-12-02 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_analysis', '0007_rename_stock_quantity_supplierproduct_quantity_supplied'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplierproduct',
            old_name='quantity_supplied',
            new_name='stock_quantity',
        ),
    ]