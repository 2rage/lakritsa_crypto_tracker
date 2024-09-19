from marketplace_monitor.models import Product


async def save_product(data):
    price = float(data['price'].replace(' ', '').replace('₽', ''))
    product = await Product.filter(title=data['title']).first()

    if product:
        difference = price - product.price
        product.price = price
        product.difference = difference
        if price < product.min_price:
            product.min_price = price
        if price > product.max_price:
            product.max_price = price
        await product.save()
    else:
        product = await Product.create(
            title=data['title'],
            price=price,
            min_price=price,
            max_price=price,
            difference=0.0,
            total_amount=price
        )
