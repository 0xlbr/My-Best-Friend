#import requests
from lxml import html
import requests

quotes_authors = {}
def get_quotes(keyWord):
    quotes = []
    authors = []
    for i in range(1, 5):
        url = "https://www.quotesdaddy.com/find/tag/" + keyWord + "/" + str(i)
        str_data = requests.get(url)
        tree = html.fromstring(str_data.content)
        page_quotes = tree.xpath('//div[@class = "quoteText"]/p/a/text()')
        page_authors = tree.xpath('//div[@class = "quoteAuthorName"]/p/a/text()')
        num_quotes = len(page_quotes)
        quotes+=page_quotes
        authors+=page_authors
    quotes = list(map(lambda q: q[1:-1], quotes))
    global quotes_authors
    quotes_authors = dict(zip(quotes, authors))
    return quotes

def get_author(topic, quote):
    quotes = get_quotes(topic)
    author  = quotes_authors.get(quote)
    return author


# for testing
#d = get_quotes("sports")
#print quotes_authors

#random_quote = d[1]
#print random_quote
#print get_author(random_quote)

#for q in get_quotes("sports"):
#    print q
#    print get_author()
