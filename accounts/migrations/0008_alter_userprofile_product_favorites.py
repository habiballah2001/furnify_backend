# Generated by Django 4.2 on 2023-05-03 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_product'),
        ('accounts', '0007_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='product_favorites',
            field=models.ManyToManyField(null=True, to='products.product'),
        ),
    ]
