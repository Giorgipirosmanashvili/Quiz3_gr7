import requests
from datetime import datetime
import json
import random
import sqlite3

def main(url):
    r = requests.get(url)
    if r.status_code != 200:
        return
    content = r.content
    j = json.loads(content)
    jstructured = json.dumps(j, indent=4)
    writejson(jstructured, 'news')
    printrandomarticle(j['articles'])
    writedb(j['articles'])


def writejson(jsoncontent, name):
    with open(f'{name}.json', 'w') as file:
        file.write(jsoncontent)

def printrandomarticle(articlelist):
    randnum = random.randint(0, len(articlelist))
    articledict = articlelist[randnum]
    print('\n\n')
    print(f'{articledict["title"]}')
    print(f'Author: {articledict["author"]}')
    print(f'Date: {articledict["publishedAt"]}')
    print(f'{articledict["description"]}')
    print(f'Link: {articledict["url"]}')

def writedb(articles):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS news
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title VARCHAR(200) NOT NULL,
                  author VARCHAR(100) NOT NULL,
                  date VARCHAR(9) NOT NULL,
                  description VARCHAR(3000) NOT NULL,
                  link VARCHAR(500))''')
    for i in articles:
        article = (i['title'], i['author'], i['publishedAt'], i['description'], i['url'])
        c.execute('INSERT INTO NEWS(title, author, date, description, link) VALUES(?, ?, ?, ?, ?)', article)
        conn.commit()
    conn.close()

if _name_ == '_main_':
    searchWord = input('შეიყვანეთ საძიებო სიტყვა: ')

    key = '3c51ee102d984d8888ccee52e529526d'

    date = input(
        'შეიყვანეთ თარიღი(ფორმატი: YYYY-MM-DD, დღევანდელი თარიღის მისათითებლად უბრალოდ დააჭირეთ ენთერს და თავისით მიეთითება default მნიშვნელობა): ')
    date = date if date else datetime.strftime(datetime.today(), '%Y-%m-%d')

    url = f'https://newsapi.org/v2/everything?q={searchWord}&from={date}&sortBy=popularity&apiKey={key}'
    main(url)