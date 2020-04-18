from bs4 import BeautifulSoup
from urllib.request import urlopen
import pickle
import os.path

word_definitions_dict = {}
word_synonyms_dict = {}

url = "https://he.wiktionary.org/wiki/%D7%9E%D7%99%D7%95%D7%97%D7%93:%D7%9B%D7%9C_%D7%94%D7%93%D7%A4%D7%99%D7%9D?from" \
      "=%D7%AA%D7%A4%D7%A1%D7%AA+%D7%9E%D7%A8%D7%95%D7%91%D7%94+%D7%9C%D7%90+%D7%AA%D7%A4%D7%A1%D7%AA&to=&namespace=0 "


def get_definitions(word, divider):
    """

    :param word:
    :param divider:
    :return:
    """
    definitions_ol = divider.find_next('ol')
    if definitions_ol is not None:
        definitions = []
        for li in definitions_ol.find_all("li"):
            dls = definitions_ol.find_all('dl')
            for dl in dls:
                dl.decompose()
            definition = str(li.get_text())
            if definition:
                definitions.append(definition.replace('\n', ''))
        word_definitions_dict[word] = definitions


def get_synonyms(word, divider):
    """

    :param word:
    :param divider:
    :return:
    """
    synonyms = divider.find(id='מילים_נרדפות')
    if synonyms is None:
        return

    synonyms_ul = synonyms.find_next('ul')
    if synonyms_ul is None:
        return

    synonyms = []
    for li in synonyms_ul.find_all('li'):
        synonym = str(li.get_text())
        if synonym:
            synonyms.append(synonym.replace('\n', ''))

    word_synonyms_dict[word] = synonyms


def scrape(origin_url, path_to_definitions, path_to_synonyms):
    """

    :param origin_url:
    :param path_to_definitions:
    :param path_to_synonyms:
    :return:
    """
    while True:
        origin_html = urlopen(origin_url)
        origin_soup = BeautifulSoup(origin_html, 'html.parser')
        words_links = origin_soup.find("div", class_="mw-allpages-body")

        for link in words_links.find_all('a'):
            word = str(link.get_text())
            if '"' in word:
                continue
            word_url = "https://he.wiktionary.org" + link.get("href")
            word_html = urlopen(word_url)
            word_soup = BeautifulSoup(word_html, 'html.parser')
            divider = word_soup.find("div", class_="mw-parser-output")
            if len(word) <= 10:
                get_definitions(word, divider)
                get_synonyms(word, divider)

        page_links = origin_soup.find("div", class_="mw-allpages-nav")
        nav_links = page_links.find_all('a')
        if len(nav_links) == 2:
            origin_url = "https://he.wiktionary.org" + nav_links[1].get('href')
        else:
            break

    with open(path_to_definitions, 'wb') as word_definitions_file, \
            open(path_to_synonyms, "wb") as word_synonyms_file:
        pickle.dump(word_definitions_dict, word_definitions_file)
        pickle.dump(word_synonyms_dict, word_synonyms_file)


def main():
    scrape(url, os.path.expanduser('~/PycharmProjects/crossword/word_definitions.p'),
           os.path.expanduser('~/PycharmProjects/crossword/word_synonyms.p'))


main()
