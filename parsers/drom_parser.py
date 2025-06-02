# drom_parser.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import logging


def get_selenium_driver():
    """Настройка ChromeDriver для работы в безголовом режиме."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def parse_drom(make, model):
    """Парсинг цен с сайта Drom.ru с использованием Selenium."""
    url = f'https://www.drom.ru/auto/marka/{make.lower()}/model/{model.lower()}/'
    driver = get_selenium_driver()

    try:
        logging.info(f"Requesting URL: {url}")
        driver.get(url)

        # Ожидаем, пока страница загрузится
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Закрываем всплывающее окно, если оно появляется
        try:
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "auth-popup__close"))
            )
            close_button.click()
            time.sleep(2)  # Подождем, чтобы окно закрылось
            logging.info("Auth-popup closed.")
        except Exception as e:
            logging.info(f"No auth-popup found, continuing... Error: {e}")

        # Парсим страницу после загрузки
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        prices = []

        # Извлекаем цены с страницы
        for item in soup.find_all('div', {'class': 'price'}):
            price = item.text.strip().replace('₽', '').replace(' ', '')
            if price.isdigit():
                prices.append(int(price))

        if not prices:
            logging.warning(f"No prices found for {make} {model}.")
        return prices

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return []

    finally:
        driver.quit()  # Закрытие драйвера всегда

