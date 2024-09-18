import csv
import json
import decimal
from datetime import datetime


def write_to_csv(data, filename='currency_data.csv'):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            data.title,
            data.price,
            data.max_price,
            data.min_price,
            data.date,
            data.difference,
            data.total_amount
        ])
    print("Данные записаны в CSV.")


def create_json_response(kash, difference, total_amount):
    return {
        "title": "Bitcoin Prices",
        "kash": kash,
        "difference": float(difference),
        "total amount": float(total_amount),
        "coins": [{"BTC": pair} for pair in ["USDT", "ETH", "XMR", "SOL", "RUB", "DOGE"]],
        "date": datetime.now().isoformat()
    }


def calculate_difference(max_price, min_price):
    return (max_price - min_price) / min_price * 100
