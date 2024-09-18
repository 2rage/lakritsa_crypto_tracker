import asyncio
import decimal
import json
from .models import CurrencyPrice
from .api_client import fetch_price
from .utils import write_to_csv, create_json_response, calculate_difference
from .email_client import send_email
from aiohttp import ClientSession


pairs = ['BTC/USDT', 'BTC/ETH', 'BTC/XMR', 'BTC/SOL', 'BTC/RUB', 'BTC/DOGE']


async def monitor_prices():
    print("Мониторинг цен начат...")
    headers = {
        'X-CMC_PRO_API_KEY': 'your_coinmarketcap_api_key',
        'Accepts': 'application/json'
    }

    for pair in pairs:
        urls = [
            f'https://api.binance.com/api/v3/ticker/price?symbol={pair.replace("/", "")}',
            f'https://api.bybit.com/v2/public/tickers?symbol={pair.replace("/", "")}',
        ]

        async with ClientSession() as session:
            tasks = [fetch_price(url, session, headers if 'coinmarketcap' in url else None) for url in urls]
            results = await asyncio.gather(*tasks)

            kash = []
            total_amount = decimal.Decimal(0)
            for result in results:
                if result:
                    price = decimal.Decimal(result['price'])
                    difference = calculate_difference(price, price)

                    # Отправляем email, если разница >= 0.03%
                    if difference >= 0.03:
                        send_email(f"Изменение курса {pair}", f"Цена: {price}, Разница: {difference}%")

                    kash.append({
                        "price": float(price),
                        "minmax": float(price),
                        "max price": float(price),
                        "max price": float(price)
                    })


                    currency_data = await CurrencyPrice.create(
                        title=pair,
                        price=price,
                        max_price=price,
                        min_price=price,
                        difference=difference,
                        total_amount=total_amount
                    )


                    write_to_csv(currency_data)


            json_data = create_json_response(kash, difference, total_amount)
            print(json.dumps(json_data, indent=4))
