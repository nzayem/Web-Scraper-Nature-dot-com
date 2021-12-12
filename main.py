import os
import string
import requests
from bs4 import BeautifulSoup as Soup


number_pages = int(input("Enter number of pages: "))

type_article = input("Enter the desired article type: ")

default_dir = os.getcwd()

for k in range(1, number_pages + 1):

    new_dir = f"Page_{str(k)}"

    os.mkdir(new_dir)

    os.chdir(new_dir)

    address = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=" + str(k)

    print(address)

    base_url = "https://www.nature.com"

    r = requests.get(address)

    soup = Soup(r.content, 'html.parser')

    links = soup.find_all('a', {'class': 'c-card__link u-link-inherit'})

    article_type = soup.find_all('span', {'class': "c-meta__type"})

    link_list = []

    type_list = []

    # getting all links
    for link in links:

        link_list.append(base_url+link.get('href'))

    # getting all articles types:

    for article in article_type:

        type_list.append(article.text)

    news_list = []

    # filtering the links to articles based on chosen type:

    for i in range(len(link_list)):

        if type_list[i] == type_article:

            news_list.append(link_list[i])

    for j in range(len(news_list)):

        req = requests.get(news_list[j])

        s = Soup(req.content, 'html.parser')

        article_body = s.find('div', {'class': "c-article-body"})

        article_title = s.find('h1')

        clean_title = f"{article_title.text.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')}.txt"

        file = open(clean_title, 'w', encoding='utf-8')

        file.write(article_body.text.strip())

        file.close()

        print(clean_title + " saved successfully")

    os.chdir(default_dir)
