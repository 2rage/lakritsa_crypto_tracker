import aiohttp


async def fetch_price(url, session, headers=None):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                
                if 'binance' in url:
                    return {'price': data['price']}
                elif 'bybit' in url:
                    return {'price': data['result'][0]['last_price']}
                elif 'gateio' in url:
                    return {'price': data[0]['last']}
                elif 'kucoin' in url:
                    return {'price': data['data']['price']}
                elif 'coinmarketcap' in url:
                    return {'price': data['data']['BTC']['quote']['USDT']['price']}
            else:
                print(f"Ошибка: не удалось получить данные с {url}, статус: {response.status}")
                return None
    except Exception as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return None
