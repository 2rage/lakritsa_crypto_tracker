import asyncio
from tortoise import Tortoise
from decouple import config
from crypto_watcher.monitor import monitor_prices


async def init():
    print("Инициализация базы данных...")
    await Tortoise.init(
        db_url=config('DATABASE_URL'),
        modules={'models': ['crypto_watcher.models']}
    )
    await Tortoise.generate_schemas()
    print("База данных инициализирована.")


async def scheduled_monitor(loop, interval):
    while True:
        await monitor_prices()
        await asyncio.sleep(interval)


def main():
    print("Запуск программы...")


    loop = asyncio.get_event_loop()


    loop.run_until_complete(init())


    interval_seconds = 10
    loop.create_task(scheduled_monitor(loop, interval_seconds))


    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Завершение программы...")
