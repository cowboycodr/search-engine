import requests
import json
import string

from bs4 import BeautifulSoup
from common import common

import threading
from urls import urls

def abort():
    return RuntimeError("aborted due to time constraints")

def spider():
    global urls
    found_urls = []
    found = 0

    
    for url in urls:
        try:
            t = threading.Timer(5, abort)
            t.start()

            url_data = requests.get(url, timeout=5)

            html = BeautifulSoup(url_data.text, "html.parser")
            hrefs = list(set([a['href'] for a in html.find_all("a", limit=3)]))


            for href in hrefs:
                if href in urls:
                    continue

                found += 1

                if href.endswith("/"):
                    href = href[:-1]

                if href.startswith("http"):
                    found_urls.append(href)

                else:

                    href = url + href
                    

                    found_urls.append(href)

                print(f"{found}. Found {href}")
        except Exception as e:
            print(e)
            continue

    urls += found_urls

# for i in range(2):
#     spider()

def craw(urls):
    data = []

    for idx, url in enumerate(urls):
        try:
            t = threading.Timer(5, abort)
            t.start()

            url_data = requests.get(url)

            html = BeautifulSoup(url_data.text, "html.parser")
            
            title = html.title.string
            text = html.body.getText()

            for special in string.punctuation:
                text = text.replace(special, "")

            data.append({
                "title": title,
                "text": text,
                "url": url
            })

            print(f"({idx + 1}/{len(urls)}) Successfully craw'd {url}")
        except Exception as e:
            print(f"Could not craw {url}")
            continue

    return data

def index(craw_data):
    data = []

    for i in craw_data:
            title = i["title"].lower()
            title_words = title.lower().split()
            text: str = i["text"].lower()
            url = i["url"]

            keywords = title_words.copy()

            for word in text.split(" "):
                word = word.lower()

                if word in keywords:
                    continue

                elif word.isnumeric():
                    continue

                elif len(word) <= 3:
                    continue

                elif word.count("\n") > 0:
                    continue

                if word in title_words:
                    keywords.append(word)

                elif text.count(word) > 3:
                    keywords.append(word)

                elif word in common:
                    continue

            data.append({
                "title": title,
                "keywords": keywords,
                "url": url
            })
    
    return data

index_data = index(craw(urls))

with open("data.json", "w") as f:
    f.write(json.dumps(index_data))