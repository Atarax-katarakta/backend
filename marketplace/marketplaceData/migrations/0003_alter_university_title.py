# Generated by Django 4.1.4 on 2023-07-29 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplaceData', '0002_alter_bank_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]
