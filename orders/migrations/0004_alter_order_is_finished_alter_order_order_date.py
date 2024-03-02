# Generated by Django 4.2 on 2023-05-07 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
