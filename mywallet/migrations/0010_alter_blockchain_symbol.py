# Generated by Django 3.2 on 2023-02-08 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mywallet', '0009_alter_wallet_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockchain',
            name='symbol',
            field=models.CharField(max_length=4, unique=True),
        ),
    ]