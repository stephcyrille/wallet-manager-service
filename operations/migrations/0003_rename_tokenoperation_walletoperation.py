# Generated by Django 3.2 on 2023-02-07 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0002_alter_tokenoperation_ops_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TokenOperation',
            new_name='WalletOperation',
        ),
    ]