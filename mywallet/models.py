import uuid
from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField


# TODO Add a boolean for giving the ability of credit or debit
class Wallet(models.Model):
    ref = models.CharField(max_length=23, blank=True, unique=True)
    code_client = models.CharField(max_length=4, blank=True)  # User start with 11 / System with 99
    owner_ref = models.CharField(max_length=36, blank=False, unique=True)
    is_active = models.BooleanField(default=False)
    fiat_amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default=0.0)
    created_date = models.DateTimeField(blank=True, editable=False, default=timezone.now)
    activated_date = models.DateTimeField(blank=True, editable=False, null=True)  # Activate by a user process

    def save(self, *args, **kwargs):
        """ On save """
        if not self.id:
            if not self.ref:
                self.ref = "W%sY%sE%s" % (str(uuid.uuid4()).split('-')[0], str(uuid.uuid4()).split('-')[1],
                                          str(uuid.uuid4()).split('-')[2])
        return super(Wallet, self).save(*args, **kwargs)

    def __str__(self):
        return self.ref


class Blockchain(models.Model):
    id_chain = models.CharField(max_length=42)
    network = models.CharField(max_length=120, blank=False, null=False)
    name = models.CharField(max_length=120, blank=False, null=False)
    symbol = models.CharField(max_length=4, blank=False, null=False, unique=True)
    currency_name = models.CharField(max_length=23, blank=False, null=False)
    url_rpc = models.URLField(blank=False, null=False)
    url_block_explorer = models.URLField(blank=False, null=False)

    def save(self, *args, **kwargs):
        """ On save """
        if not self.id:
            self.id_chain = 'CHAIN-%s' % (str(uuid.uuid4()))
        return super(Blockchain, self).save(*args, **kwargs)

    def __str__(self):
        return "%s-%s" % (self.network, self.name)


class Token(models.Model):
    ref = models.CharField(max_length=42)
    name = models.CharField(max_length=23)
    symbol = models.CharField(max_length=4)
    id_blockchain = models.CharField(max_length=42)
    unit_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def save(self, *args, **kwargs):
        """ On save """
        if not self.id:
            self.ref = 'TOKEN-%s' % (str(uuid.uuid4()))
        return super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return "%s-%s" % (self.symbol, self.name)


class EntityToken(models.Model):
    token_symbol = models.CharField(max_length=4)
    token_ref = models.CharField(max_length=42, blank=False)
    wallet_ref = models.CharField(max_length=23, blank=False)
    owner_ref = models.CharField(max_length=36, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # 125.05
    fiat_value = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default=0.0)
    is_active = models.BooleanField(default=False)
    activated_date = models.DateTimeField(blank=True, editable=False, null=True)  # Activate by a user process

    def __str__(self):
        return "(%s) %s" % (self.token_symbol, self.owner_ref.split('-')[0])

