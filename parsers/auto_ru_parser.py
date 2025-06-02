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

# Список прокси (можно закомментировать, если не хотите использовать прокси)
PROXIES = [
    "http://10.10.1.10:3128",
    "http://20.20.2.2:3128",
]


# Функция для получения случайного User-Agent
def get_random_user_agent():
    return random.choice(USER_AGENTS)


# Функция для получения случайного прокси
def get_random_proxy():
    return random.choice(PROXIES)


def parse_auto_ru(make, model):
    url = f'https://auto.ru/moskva/cars/?make_id={make}&model_id={model}'

    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept-Language': 'en-US,en;q=0.9'
    }

    # Использование прокси
    # Если хотите отключить прокси, закомментируйте следующие строки:
    # proxy = get_random_proxy()
    # proxies = {"http": proxy, "https": proxy}

    # Отправка запроса с прокси (если используете)
    proxies = None  # Отключить прокси для тестирования
    try:
        # Выполняем запрос
        response = requests.get(url, headers=headers, proxies=proxies)

        # Обработка ошибки 429 (слишком много запросов)
        if response.status_code == 429:
            logging.warning(f"Too many requests, waiting before retrying...")
            time.sleep(30)  # Задержка 30 секунд перед повтором
            response = requests.get(url, headers=headers, proxies=proxies)

        response.raise_for_status()  # Возбуждает исключение при ошибке HTTP

    except requests.RequestException as e:
        logging.error(f"Error fetching data from Auto.ru: {e}")

        # Проверяем существует ли переменная response перед её использованием
        if 'response' in locals():
            logging.error(f"Response status code: {response.status_code}")
        else:
            logging.error("No response object created due to error.")

        # Прерывание выполнения и вывод исключения
        raise Exception("Failed to fetch data from Auto.ru")

    # Парсим HTML-страницу
    soup = BeautifulSoup(response.text, 'html.parser')
    prices = []

    # Ищем все элементы с ценой
    for item in soup.find_all('span', {'class': 'price'}):
        price = item.text.strip().replace('₽', '').replace(' ', '')  # Убираем символы и пробелы
        if price.isdigit():  # Проверяем, является ли цена числом
            prices.append(int(price))

    # Возвращаем список найденных цен
    return prices
