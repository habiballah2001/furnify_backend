# Generated by Django 4.2 on 2023-05-07 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_remove_userprofile_id_alter_city_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]