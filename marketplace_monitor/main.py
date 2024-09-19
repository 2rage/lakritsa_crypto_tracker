import asyncio
from tortoise import Tortoise
from decouple import config
from marketplace_monitor.spiders import WildberriesSpider, OzonSpider
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process


def run_scrapy_spider():
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    })
    process.crawl(OzonSpider)
    process.start()


async def init():
    try:
        print("Инициализация базы данных...")
        await Tortoise.init(
            db_url=config('DATABASE_URL2'),
            modules={'models': ['marketplace_monitor.models']}
        )
        await Tortoise.generate_schemas()
        print("База данных инициализирована.")
    except Exception as e:
        raise RuntimeError(f"Ошибка инициализации базы данных: {str(e)}")


def run_scrapy_spider():
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    })
    process.crawl(WildberriesSpider)
    process.start()


async def scheduled_monitor(interval):
    while True:
        try:
            print("Мониторинг цен...")
            process = Process(target=run_scrapy_spider)
            process.start()
            process.join()
        except Exception as e:
            raise RuntimeError(f"Ошибка мониторинга цен: {str(e)}")
        await asyncio.sleep(interval)


def main():
    try:
        print("Запуск программы...")

        loop = asyncio.get_event_loop()

        loop.run_until_complete(init())

        interval_seconds = 600
        loop.create_task(scheduled_monitor(interval_seconds))

        loop.run_forever()
    except KeyboardInterrupt:
        print("Завершение программы...")
    except Exception as e:
        raise RuntimeError(f"Ошибка выполнения программы: {str(e)}")
    finally:
        loop.run_until_complete(Tortoise.close_connections())
        print("Соединение с базой данных закрыто.")
