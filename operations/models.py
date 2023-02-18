import uuid
from django.db import models
from django.utils import timezone

OPS_CHOICES = (
    ("TOP_UP", "Top up"),  # From an internal wallet to client wallet (so we need to check if it is an internal wallet
    ("FIAT_TOP_UP", "Fiat Top up"),  # From an internal wallet to client wallet
    ("WIRE_TRANSFER", "Wire Transfer"),  # Between two clients
    ("FIAT_WIRE_TRANSFER", "Fiat Wire Transfer"),  # Between two clients
    ("WITHDRAW", "Withdraw"),  # Remove from internal remove wallet to a client wallet
    ("FIAT_WITHDRAW", "Fiat Withdraw"),  # Remove from internal remove wallet to a client wallet
)
PAYMENT_NAME = (
    ("MTNMOMO", "MTN Mobile money"),
    ("OM", "Orange Money"),
    ("MASTERCARD", "Mastercard"),
    ("VISA", "Visa Card"),
    ("PAYPAL", "Paypal"),
)
OPERATOR_TYPES = (
    ("BANK", "Bank"),
    ("MOMO", "Mobile money"),
)


class PaymentMethod(models.Model):
    operator = models.CharField(max_length=25, choices=OPERATOR_TYPES, blank=False)
    name = models.CharField(max_length=25, blank=False, choices=PAYMENT_NAME)
    reason = models.CharField(max_length=50, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)  # TODO we must encrypt the card number
    card_CVV = models.CharField(max_length=3, blank=True, null=True)  # TODO we must encrypt the card number
    card_owner = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    card_expiry_date = models.CharField(max_length=5, blank=True, null=True)


class WalletOperation(models.Model):
    trx_ref = models.CharField(max_length=44)
    ops_type = models.CharField(max_length=18, choices=OPS_CHOICES)
    from_wallet = models.CharField(max_length=23, blank=False)
    # When we will make a withdrawal, the destination wallet will be an internal specific wallet
    to_wallet = models.CharField(max_length=23, blank=False)
    to_external_wallet = models.CharField(max_length=42, blank=True)
    # TODO create a blockchain ID specified for fiat operation
    id_blockchain = models.CharField(max_length=42, blank=False)
    token_code = models.CharField(max_length=5, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_date = models.DateTimeField(blank=True, editable=False, default=timezone.now)

    def save(self, *args, **kwargs):
        """ On save """
        if not self.id:
            self.trx_ref = 'OPS_TOK-%s' % (str(uuid.uuid4()))
        return super(WalletOperation, self).save(*args, **kwargs)

    def __str__(self):
        return "(%s) %s" % (self.ops_type, self.trx_ref)
