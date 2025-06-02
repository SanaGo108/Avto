import pandas as pd
import requests
from bs4 import BeautifulSoup

# Пример URL для парсинга (замените на реальный)
url = "https://www.avito.ru/moskva/avtomobili"


# Функция для парсинга данных с сайта
def parse_data(url):
    # Отправляем запрос на сайт
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Пример парсинга: находим все объявления
    cars = soup.find_all('div', {'class': 'item_table'})

    data = []

    for car in cars:
        model = car.find('h3').get_text()  # Находим модель автомобиля
        price = car.find('span', {'class': 'price'}).get_text()  # Находим цену
        link = car.find('a')['href']  # Ссылка на объявление

        # Добавляем данные в список
        data.append({'Модель': model, 'Стоимость': price, 'Ссылка': link})

    return data


# Собираем данные с сайта
cars_data = parse_data(url)

# Создаем DataFrame из данных
df = pd.DataFrame(cars_data)

# Печать таблицы
print(df)

# Сохраняем данные в CSV файл
df.to_csv('cars_data.csv', index=False)
