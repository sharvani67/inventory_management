# Generated by Django 5.1.3 on 2024-12-08 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_analysis', '0011_delete_customer_sale_customer_mobile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellingPriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fixed_selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('supplier_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock_analysis.supplierproduct')),
            ],
        ),
    ]
