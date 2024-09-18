from crypto_watcher.models import CurrencyPrice


async def get_all_prices():
    return await CurrencyPrice.all()


async def get_price_by_id(price_id):
    return await CurrencyPrice.get(id=price_id)


async def update_price(price_id, **kwargs):
    price = await CurrencyPrice.get(id=price_id)
    for key, value in kwargs.items():
        setattr(price, key, value)
    await price.save()


async def delete_price(price_id):
    price = await CurrencyPrice.get(id=price_id)
    await price.delete()
