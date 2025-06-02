import requests
from bs4 import BeautifulSoup
import logging
import time
import random

# Список User-Agent для случайного выбора
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def fetch_with_retry(url, headers, retries=5, delay=60):
    attempt = 0
    while attempt < retries:
        try:
            # Отправляем запрос
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()  # Проверка успешного статуса
            return response
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                logging.warning(f"Too many requests. Retrying in {delay} seconds...")
                time.sleep(delay)  # Задержка перед повторной попыткой
            elif response.status_code == 503:
                logging.warning(f"Service unavailable. Retrying in {delay} seconds...")
                time.sleep(delay)  # Задержка при недоступности сервиса
            else:
                logging.error(f"Request failed: {e}")
                time.sleep(delay)
            attempt += 1
    raise Exception(f"Failed to fetch data after {retries} attempts")

def parse_auto_ru(make, model):
    url = f'https://auto.ru/moskva/cars/?make_id={make}&model_id={model}'

    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept-Language': 'en-US,en;q=0.9'
    }

    try:
        logging.info(f"Fetching data for {make} {model} from Auto.ru...")
        time.sleep(random.uniform(120, 180))  # Задержка от 2 до 3 минут

        # Используем retry-систему для запросов
        response = fetch_with_retry(url, headers)

        # Парсим HTML-страницу с помощью BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        prices = []

        # Ищем все элементы с ценой
        for item in soup.find_all('span', {'class': 'price'}):
            price = item.text.strip().replace('₽', '').replace(' ', '')  # Убираем символы и пробелы
            if price.isdigit():  # Проверяем, является ли цена числом
                prices.append(int(price))  # Добавляем цену в список

        return prices

    except Exception as e:
        logging.error(f"Error fetching data from Auto.ru: {e}")
        return []

