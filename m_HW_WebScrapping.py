# Домашнее задание к лекции 6. «Web-scrapping»

import requests
import bs4  # библиотека beautifulsoup4 - будемиспользовать для парсинга днных вместо регулярных выражений
import lxml  # библиотека движок для beautifulsoup4, без неё неработает beautifulsoup4
import fake_headers  # библиотека для формирования загловков, чтобы сайт не думал что мы робот

from pprint import pprint


# Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# функция для генерации заголовков(с пмощью fake_headers)
def gen_headers():
    headers_gen = fake_headers.Headers(os='win', browser='chrome')  # передаём в перемнные нашу операционку и браузер которым пользуемся
    return headers_gen.generate()  # генерация слваря

# Функция парснга хабра по ключевым словам
def pars_habr():
    URL = 'https://habr.com/ru/articles/'

    response = requests.get(URL, headers=gen_headers())  # а вот тут добавим в параметр headers= библиотеку fake-headers - для того чтобы сайт нас не заблокировал как робота

    # Структурируем наши запросы чтобы небыло путаницы
    main_html = response.text  # main_html - наша страница со всеми статьями
    main_page = bs4.BeautifulSoup(main_html, features='lxml')
    article_list_tag = main_page.find(name='div', class_='tm-articles-list')  # <div class="tm-articles-list"> - путь поиска статей
    article_tags = article_list_tag.find_all('article')  # сюда добавляем наши статьи и по ним можно будет итерироваться

    article_data = []  # список наших извлечённых данных

    for article_tag in article_tags:
        # Извлеаем теги, а позже извлечём из них конкретику
        h2_tag = article_tag.find(name='h2', class_='tm-title tm-title_h2')  # извлекаем класс <h2 class="tm-title tm-title_h2">, а из него извлечём всё остальне
        a_tag = h2_tag.find(name='a')  # здесь будет ссылка этой статьи <a href="/ru/companies/kaspersky/articles/793104/", но заберём её ПОЗЖЕ через список
        tag_span = h2_tag.find(name='span')  # здесь будет текст заголова
        time_tag = article_tag.find(name='time')  # здесь будет время пубикации статьи
        
        # конкретика
        link_relative = a_tag['href']  # обращемся к тегу a_tag за ссылкой
        link_absolute = f'https://habr.com{link_relative}'  # деаем ссылку абсолютной
        header = tag_span.text.strip()  # извлекаем текст заголовка
        pub_time = time_tag['datetime']
        
        # Извлекаем полный текст статьи
        response = requests.get(link_absolute, headers=gen_headers()) 
        article_html = response.text
        article_page = bs4.BeautifulSoup(article_html, features='lxml')
        article_body_tag = article_page.find(name='div', id='post-content-body')
        artcle_text = article_body_tag.text.strip()
        
        # добавляем в наш список извлечённые данные по ключевым словам в заголвке и тексте
        for elem in KEYWORDS:
            s_low_reg_head = header.lower()  # приведение к нижним регистрам как в списке KEYWORDS
            s_low_reg_text = artcle_text.lower()
            
            if s_low_reg_head.count(elem):  # Добавлен ключ 'Count KEYWORDS' для понимания где встретилось ключевое слово, в заголовке или тексте
                article_data.append({
                    'Count KEYWORDS': 'Header',
                    'pubtime': pub_time,
                    'header': header,
                    'link': link_absolute
                    })
                
            if s_low_reg_text.count(elem):
                article_data.append({
                    'Count KEYWORDS': 'Text',
                    'pubtime': pub_time,
                    'header': header,
                    'link': link_absolute
                    })
        
    pprint(article_data, width=240, sort_dicts=False)  # выводим данные без сортировки(нам нужно: <дата> – <заголовок> – <ссылка>)
    
pars_habr()




















## Ваш код