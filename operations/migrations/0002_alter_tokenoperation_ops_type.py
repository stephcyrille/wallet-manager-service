# Generated by Django 3.2 on 2023-02-02 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenoperation',
            name='ops_type',
            field=models.CharField(choices=[('TOP_UP', 'Top up'), ('WIRE_TRANSFER', 'Wire Transfer'), ('P2P_TRANSFER', 'Peer To Peer Transfer'), ('WITHDRAW', 'Withdraw')], max_length=14),
        ),
    ]
