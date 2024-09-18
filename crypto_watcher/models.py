from tortoise import fields, Model


class CurrencyPrice(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50)
    price = fields.DecimalField(max_digits=18, decimal_places=8)
    max_price = fields.DecimalField(max_digits=18, decimal_places=8)
    min_price = fields.DecimalField(max_digits=18, decimal_places=8)
    difference = fields.DecimalField(max_digits=18, decimal_places=8)
    total_amount = fields.DecimalField(max_digits=18, decimal_places=8)
    date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "currency_prices"
