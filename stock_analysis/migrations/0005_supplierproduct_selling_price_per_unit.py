# Generated by Django 5.1.3 on 2024-12-02 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_analysis', '0004_remove_sale_product_remove_supplierproduct_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierproduct',
            name='selling_price_per_unit',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
