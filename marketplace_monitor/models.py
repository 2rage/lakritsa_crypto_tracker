from tortoise import fields, models


class Product(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    min_price = fields.DecimalField(max_digits=10, decimal_places=2)
    max_price = fields.DecimalField(max_digits=10, decimal_places=2)
    date = fields.DatetimeField(auto_now_add=True)
    difference = fields.DecimalField(max_digits=10, decimal_places=2)
    total_amount = fields.DecimalField(max_digits=20, decimal_places=8)

    class Meta:
        table = "products"