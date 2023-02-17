# Generated by Django 3.2 on 2023-02-16 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0004_auto_20230208_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('MOMO', 'MTN Mobile money'), ('OM', 'Orange Money'), ('MASTERCARD', 'Mastercard'), ('VISA', 'Visa Card'), ('PAYPAL', 'Paypal')], max_length=25)),
                ('operator', models.CharField(blank=True, max_length=50, null=True)),
                ('reason', models.CharField(blank=True, max_length=50, null=True)),
                ('card_number', models.CharField(blank=True, max_length=50, null=True)),
                ('card_CVV', models.CharField(blank=True, max_length=3, null=True)),
                ('card_owner', models.CharField(blank=True, max_length=150, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('card_expiry_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
