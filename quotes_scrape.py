#import requests
from lxml import html
import requests


def get_quotes(keyWord):
    quotes = []
    for i in range(1, 5):
        url = "https://www.quotesdaddy.com/find/tag/" + keyWord + "/" + str(i)
        str_data = requests.get(url)
        tree = html.fromstring(str_data.content)
        page_quotes = tree.xpath('//div[@class = "quoteText"]/p/a/text()')
        num_quotes = len(page_quotes)
        quotes+=page_quotes
    quotes = list(map(lambda q: q[1:-1], quotes))
    return quotes



for q in get_quotes("sports"):
    print q
