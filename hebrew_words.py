"""
Filename: hebrew_words.py
Purpose: Generate Hebrew language vocabulary and sort by frequency in Wikipedia scrape
Author: I.C.
Date: 15.04.2020
"""

from bs4 import BeautifulSoup
from collections import Counter
import re
import os

INVALID_FILENAME_PATTERN = re.compile(r'\.(jpg|png)\.html$|שיחת_משתמש|תמונה')
PARAGRAPHS_PATTERN = re.compile(r"<p>(.*?)</p>")
CHARS_PATTERN = re.compile(r"""[^אבגדהוזחטיכלמנסעפצקרשתןףץםך'\-\s"]""")
MOSHE_AND_DOG = ['מ', 'ש', 'ה', 'ו', 'כ', 'ל', 'ב']


def variations(word):
    return [(character + word) for character in MOSHE_AND_DOG]


def passes_criteria(word, freq):
    if word[0] in MOSHE_AND_DOG and word[1:] in freq.keys() and len(word) > 3:
        return False
    return True


def create_words_document(amount=100000):
    all_files = []
    for root, _, filenames in os.walk(u'wikipedia-he-html'):
        for filename in filenames:
            if INVALID_FILENAME_PATTERN.search(filename):
                continue
            all_files.append(os.path.join(root, filename))

    freq = Counter()

    for i, file_path in enumerate(all_files):

        try:
            html = open(file_path, "rb").read().decode('utf8')
        except UnicodeDecodeError:
            continue

        if '<meta http-equiv="Refresh"' in html:  # HTML redirect
            continue

        for p_html in PARAGRAPHS_PATTERN.findall(html):
            p_text = BeautifulSoup(p_html, 'html.parser').get_text()
            p_text = CHARS_PATTERN.sub('', p_text)
            for word in p_text.split():
                word = word.strip('="')
                if len(word) > 1:
                    if passes_criteria(word, freq):
                        freq[word] += 1
                    else:
                        freq[word[1:]] += 1

    print("Total words found: ", len(freq))
    with open("words.txt", "wb") as words_file:
        words_file.write(u"\n".join("%s" % word for (word, frequency) in freq.most_common(amount)).encode('utf8'))

    return freq
