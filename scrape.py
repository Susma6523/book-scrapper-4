#pip3 install --upgrade pip
#=> get data from web9html,json,xml)
#python3 -m pip install beautifulsoup4
#=> parse html

#Git tutorial
#git config--global user.name "susma shrestha"
#git config --gobal user.email "susmastha4@"
#git init
#git status => if you want to check what are the changes
# git diff => if you want to check what are the changes
#git add .
#git commit -m "your message"
#copy paste git from github


###################
#1. change the code
#2. git add.
##git commit -m "your message"
# git push origin

import sqlite3
import requests


from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"

def create_database():
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, 
            price REAL,
            currency TEXT
        )
    """
    )

    conn.commit()
    conn.close()

def insert_book(title, price, currency):
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO books (title, price, currency) VALUES(?,?,?)
    """,
        (title, price, currency),
    )

    conn.commit()
    conn.close()

def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page, status code:{response.status_code}")
        return


    response.encoding = response.apparent_encoding 
    print(response.text)


    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_ = "price_color").text

        #extract currency and numeric part
        # the first char should be the currency symbol(eg, £ )

        currency = price_text[0]
        price = price_text[1:]


        insert_book(title, price, currency)

create_database()
        

scrape_books(URL)


