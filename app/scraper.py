import urllib

from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()


def encode(s): return urllib.parse.quote(s)


class Scraper:
    @staticmethod
    def steam(term):
        url = 'https://store.steampowered.com/search/?term=' + encode(term)

        r = session.get(url)
        soup = BeautifulSoup(r.html.html, 'html.parser')

        results = []

        entries = soup.select('#search_resultsRows a')[:10]
        for entry in entries:
            link = entry['href']
            img_url = entry.select('.search_capsule img')[0]['src']
            title = entry.select('.responsive_search_name_combined .search_name')[0].text.strip()
            price = entry.select('.responsive_search_name_combined .search_price_discount_combined')[0]['data-price-final']

            result = {'link': link,
                      'img_url': img_url,
                      'title': title,
                      'price': '$' + str(float(price) / 100)}
            results.append(result)

        return results
