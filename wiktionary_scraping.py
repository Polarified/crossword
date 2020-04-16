from bs4 import BeautifulSoup
from collections import Counter
import re
import os
from urllib.request import urlopen

# So: I need to start from a page. Go over each item and read it's value. Filter out those with "s.
# Then, go into that page. Get both the synonyms and the definition.
# Then exit out and continue over the whole page.
# Once done with the page, move onto the next page. All the way until there is no next page link.

url = "https://he.wiktionary.org/wiki/%D7%9E%D7%99%D7%95%D7%97%D7%93:%D7%9B%D7%9C_%D7%94%D7%93%D7%A4%D7%99%D7%9D?from" \
      "=%D7%90&to=&namespace=0 "
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

soup = soup.find_all("div", class_="mw-allpages-body")
