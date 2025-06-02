import argparse
import logging
from parsers.avito_parser import parse_avito
from parsers.auto_ru_parser import parse_auto_ru
from parsers.drom_parser import parse_drom
from calculator import calculate_collateral
from logger import setup_logger
from database import insert_car_price

import concurrent.futures

def fetch_data_parallel(make, model):
    """Использует многозадачность для параллельного получения данных с сайтов."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_avito = executor.submit(parse_avito, make, model)
        future_auto_ru = executor.submit(parse_auto_ru, make, model)
        future_drom = executor.submit(parse_drom, make, model)

        avito_prices = future_avito.result()
        auto_ru_prices = future_auto_ru.result()
        drom_prices = future_drom.result()

    return avito_prices, auto_ru_prices, drom_prices

def save_to_db(make, model, prices, collateral_value):
    """Сохраняет данные в базу данных"""
    for price in prices:
        insert_car_price(make, model, price, collateral_value)

def main(make, model):
    logger = setup_logger()
    logger.info(f"Starting main function for {make} {model}")
    print(f"Starting main function for {make} {model}")

    try:
        # Печатаем все шаги
        logger.info(f"Fetching data for {make} {model}")
        print(f"Fetching data for {make} {model}")

        # Получаем данные параллельно
        avito_prices, auto_ru_prices, drom_prices = fetch_data_parallel(make, model)

        # Печатаем результат
        print(f"Avito prices: {avito_prices}")
        print(f"Auto.ru prices: {auto_ru_prices}")
        print(f"Drom.ru prices: {drom_prices}")

        logger.info(f"Avito prices: {avito_prices}")
        logger.info(f"Auto.ru prices: {auto_ru_prices}")
        logger.info(f"Drom.ru prices: {drom_prices}")

        # Объединяем все данные
        prices = avito_prices + auto_ru_prices + drom_prices

        if not prices:
            logger.warning(f"No prices found for {make} {model}")
            print(f"No prices found for {make} {model}")

        average_price, collateral_value = calculate_collateral(prices)

        result = {
            "make": make,
            "model": model,
            "average_price": average_price,
            "collateral_value": collateral_value,
            "cars_parsed": len(prices)
        }

        print(result)
        logger.info(f"Completed for {make} {model}: {result}")

        # Сохраняем результаты в БД
        save_to_db(make, model, prices, collateral_value)

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate car collateral value")
    parser.add_argument('--make', required=True, help='Car make')
    parser.add_argument('--model', required=True, help='Car model')
    args = parser.parse_args()

    main(args.make, args.model)
