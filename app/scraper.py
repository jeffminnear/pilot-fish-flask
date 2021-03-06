import urllib
import requests
import json

from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()
session.browser


def encode(s): return urllib.parse.quote(s)


def get_soup(url):
    r = session.get(url)
    r.html.render()
    return BeautifulSoup(r.html.html, 'html.parser')


class Scraper:
    @staticmethod
    def steam(term):
        url = 'https://store.steampowered.com/search/?term=' + encode(term)

        soup = get_soup(url)

        results = []

        i = 1
        entries = soup.select('#search_resultsRows a')[:10]
        for entry in entries:
            link = entry['href']
            img_url = entry.select('.search_capsule img')[0]['src']
            title = entry.select('.responsive_search_name_combined .search_name')[0].text.strip()

            price = entry.select('.responsive_search_name_combined .search_price_discount_combined')[0]['data-price-final']

            result = {'link': link,
                      'img_url': img_url,
                      'title': title,
                      'price': (float(price) / 100),
                      'store': 1,
                      'sort_order': i}
            results.append(result)
            i += 1

        return results

    @staticmethod
    def gog(term):
        base_url = 'https://www.gog.com'
        search_url = base_url + '/games/ajax/filtered?limit=20&search=' + encode(term)

        response = json.loads(requests.get(search_url).text)
        entries = response['products']

        results = []

        i = 1
        for entry in entries:
            result = {'link': base_url + entry['url'],
                      'img_url': 'http:' + entry['image'] + '.jpg',
                      'title': entry['title'],
                      'price': float(entry['price']['amount']),
                      'store': 3,
                      'sort_order': i}

            results.append(result)
            i += 1

        return results

    @staticmethod
    def fanatical(term):
        base_url = 'https://www.fanatical.com'
        search_url = base_url + '/en/search?search=' + encode(term)

        soup = get_soup(search_url)

        results = []

        i = 1
        entries = soup.select('.ais-Hits__root > .card-container')[:10]
        for entry in entries:
            link = entry.select('a.faux-block-link__overlay-link')[0]['href']

            image_object = entry.select('.responsive-image img.img-fluid')[0]
            img_url = image_object['src']
            title = image_object['alt']

            price = entry.select('span.card-price')[0].text.replace('$', '')

            result = {'link': base_url + link,
                      'img_url': img_url,
                      'title': title,
                      'price': float(price),
                      'store': 4,
                      'sort_order': i}

            results.append(result)
            i += 1

        return results

    @staticmethod
    def greenmangaming(term):
        base_url = 'https://www.greenmangaming.com'
        search_url = base_url + '/search/' + encode(term)

        soup = get_soup(search_url)

        results = []

        i = 1
        entries = soup.select('ul.table-search-listings > li')[:10]
        for entry in entries:
            media_object = entry.select('.media-object')[0]
            link = media_object.select('a')[0]['ng-href']
            img_url = media_object.select('img')[0]['ng-src']

            title = entry.select('.prod-name')[0].text.strip()

            price = entry.select('price.notranslate')[0].text.strip().replace('$', '')

            result = {'link': base_url + link,
                      'img_url': img_url,
                      'title': title,
                      'price': float(price),
                      'store': 2,
                      'sort_order': i}

            results.append(result)
            i += 1

        return results
