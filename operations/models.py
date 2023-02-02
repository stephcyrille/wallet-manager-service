import uuid
from django.db import models
from django.utils import timezone

OPS_CHOICES = (
    ("TOP_UP", "Top up"),  # From an internal wallet to client wallet (so we need to check if it is an internal wallet
    ("WIRE_TRANSFER", "Wire Transfer"),  # From internal specified wallet to client wallet
    ("P2P_TRANSFER", "Peer To Peer Transfer"),  # Between two clients
    ("WITHDRAW", "Withdraw"),  # Remove from internal remove wallet to a client wallet
)


class TokenOperation(models.Model):
    trx_ref = models.CharField(max_length=44)
    ops_type = models.CharField(max_length=14, choices=OPS_CHOICES)
    from_wallet = models.CharField(max_length=23, blank=False)
    to_wallet = models.CharField(max_length=23, blank=False)
    id_blockchain = models.CharField(max_length=42, blank=False)
    token_code = models.CharField(max_length=5, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_date = models.DateTimeField(blank=True, editable=False, default=timezone.now)

    def save(self, *args, **kwargs):
        """ On save """
        if not self.id:
            self.trx_ref = 'OPS_TOK-%s' % (str(uuid.uuid4()))
        return super(TokenOperation, self).save(*args, **kwargs)

    def __str__(self):
        return "(%s) %s" % (self.ops_type, self.trx_ref)

