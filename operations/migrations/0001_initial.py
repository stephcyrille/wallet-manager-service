# Generated by Django 3.2 on 2023-02-20 17:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WalletOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trx_ref', models.CharField(max_length=44)),
                ('ops_type', models.CharField(choices=[('TOP_UP', 'Top up'), ('FIAT_TOP_UP', 'Fiat Top up'), ('WIRE_TRANSFER', 'Wire Transfer'), ('FIAT_WIRE_TRANSFER', 'Fiat Wire Transfer'), ('WITHDRAW', 'Withdraw'), ('FIAT_WITHDRAW', 'Fiat Withdraw')], max_length=18)),
                ('from_wallet', models.CharField(max_length=23)),
                ('to_wallet', models.CharField(max_length=23)),
                ('to_external_wallet', models.CharField(blank=True, max_length=42)),
                ('id_blockchain', models.CharField(max_length=42)),
                ('token_code', models.CharField(max_length=5)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PENDING', 'Pending'), ('SUCCEED', 'Succeed'), ('FAILED', 'Failed'), ('CANCELED', 'Canceled')], default='DRAFT', max_length=10)),
                ('details', models.TextField(blank=True)),
            ],
        ),
    ]
