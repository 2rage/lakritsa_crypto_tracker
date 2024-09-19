import logging
import aiomail
from decouple import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def notify(price_diff, product):
    if price_diff >= 0.03:
        message = aiomail.Message(
            subject="Price Alert!",
            body=f"The price of {product.title} has changed significantly by {price_diff:.2%}",
            to=config('NOTIFY_EMAIL')
        )
        smtp = aiomail.SMTP(hostname=config('SMTP_HOST'), port=config('SMTP_PORT'))
        await smtp.send(message)
        await smtp.quit()


async def log_product_change(product):
    logger.info(f"Product: {product.title} - New price: {product.price}, Change: {product.difference}")
