from bs4 import BeautifulSoup
from collections import Counter
import re
import os
from urllib.request import urlopen

# So: I need to start from a page. Go over each item and read it's value. Filter out those with "s.
# Then, go into that page. Get both the synonyms and the definition.
# Then exit out and continue over the whole page.
# Once done with the page, move onto the next page. All the way until there is no next page link.

word_definitions_dict = {}
word_synonyms_dict = {}

url = "https://he.wiktionary.org/wiki/%D7%9E%D7%99%D7%95%D7%97%D7%93:%D7%9B%D7%9C_%D7%94%D7%93%D7%A4%D7%99%D7%9D?from" \
      "=%D7%90%D7%91+%D7%94%D7%A2%D7%95%D7%A8%D7%A7%D7%99%D7%9D&to=&namespace=0 "
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

soup = soup.find("div", class_="mw-allpages-body")
for link in soup.find_all('a'):
    word = link.get_text()
    word_url = "https://he.wiktionary.org" + link.get("href")
    word_html = urlopen(word_url)
    word_soup = BeautifulSoup(word_html, 'html.parser')
    divider = word_soup.find("div", class_="mw-parser-output")
    definition = divider.find_next('ol')
    if definition is not None:
        definitions = []
        for li in definition.find_all("li"):
            dls = definition.find_all('dl')
            for dl in dls:
                dl.decompose()
            definitions.append(li.get_text())
        word_definitions_dict[word] = definitions

for k, v in word_definitions_dict.items():
    print(k, v)
