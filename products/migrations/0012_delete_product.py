# Generated by Django 4.2 on 2023-05-02 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_delete_userprofile'),
        ('orders', '0002_remove_orderdetails_order_and_more'),
        ('products', '0011_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]
