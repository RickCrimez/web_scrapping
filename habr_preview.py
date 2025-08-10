import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


# Проверяем наличие ключевых слов:
def contains_keywords(text):
    text = text.lower()
    return any(keyword.lower() in text for keyword in KEYWORDS)


# Парсинг страницы Habr'a:
url = 'https://habr.com/ru/articles/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    for article in articles:
        title_element = article.find('h2')
        if not title_element:
            continue

        title = title_element.text.strip()
        link = title_element.find('a')['href']
        if not link.startswith('http'):
            link = 'https://habr.com' + link

        time_element = article.find('time')
        if time_element:
            date_str = time_element['datetime']
            date = datetime.fromisoformat(date_str).strftime('%Y-%m-%d')
        else:
            date = 'N/A'

        preview_text = ''
        preview_element = article.find('div', class_='article-formatted-body')
        if preview_element:
            preview_text = preview_element.text.strip()

        if contains_keywords(title) or contains_keywords(preview_text):
            print(f'{date} – {title} – {link}')

except requests.exceptions.RequestException as e:
    print(f'Ошибка при запросе к Хабра: {e}')
except Exception as e:
    print(f'Произошла ошибка: {e}')