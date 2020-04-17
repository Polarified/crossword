"""
Filename: main.py
Purpose: Generate a Hebrew vocabulary, create definitions, and place in crossword, then display it.
Author: I.C.
Date: 15.04.2020
"""

import pickle

# from hebrew_words import create_words_document
from word_creation_algorithms import find_matches
# from wiktionary_scraping import scrape


def main():
    print("Crossword Word-Def Generation")
    # menu = {1: create_words_document, 2: scrape, 3: find_matches}
    # word_gen = int(
    #     input("For a Hebrew language, enter 1. For a Wiktionary scrape, enter 2. To create definitions, enter 3."))
    # if word_gen == "y" or word_gen == "n":
    #     if word_gen == "y":
    #         create_words_document("~/Data/wikipedia-he-html", "hebrew_words_dump.p")

    matches = {}

    with open("word_definitions.p", "rb") as word_definitions_file, open("word_synonyms.p", "rb") as word_synonyms_file:
        word_definitions = pickle.load(word_definitions_file)
        word_synonyms = pickle.load(word_synonyms_file)
        words = list(word_definitions.keys())
        definitions = list(word_definitions.values())
        synonyms = list(word_synonyms.values())

        find_matches(words, matches)
        print(matches)

    # else:
    #     print("Bad input. Exiting.")


if __name__ == '__main__':
    main()
