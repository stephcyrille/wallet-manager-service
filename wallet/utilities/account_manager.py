from decimal import Decimal


def move_token(origin, destination, amount):
    if origin.amount.amount >= Decimal.from_float(float(amount)):
        origin.amount.amount -= Decimal.from_float(float(amount))
        destination.amount.amount += Decimal.from_float(float(amount))
        origin.save()
        destination.save()
        return True
    else:
        return False


def move_fiat(origin, destination, amount):
    if origin.fiat_amount.amount >= Decimal.from_float(float(amount)):
        origin.fiat_amount.amount -= Decimal.from_float(float(amount))
        destination.fiat_amount.amount += Decimal.from_float(float(amount))
        origin.save()
        destination.save()
        return True
    else:
        return False

