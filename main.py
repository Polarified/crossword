"""
Filename: main.py
Purpose: Generate a Hebrew vocabulary, create definitions, and place in crossword, then display it.
Author: I.C.
Date: 15.04.2020
"""

from hebrew_words import create_words_document
from word_creation_algorithms import find_matches


def main():
    print("Crossword Word-Def Generation")
    word_gen = input("Would you like to create a list of words in the hebrew language from a Wikipedia crawl? [y/n]: ")
    if word_gen == "y" or word_gen == "n":
        if word_gen == "y":
            amount = 100000
            try:
                amount = int(input("Enter the amount of words from the Hebrew language you would like to include: "))
            except ValueError:
                print("Invalid amount entered. Proceeding with default(100000).")
            create_words_document(amount, "~/Data/wikipedia-he-html")

        matches = {}

        with open("words.txt", "rb") as words_file:
            vocabulary = [line.decode()[:-1] for line in words_file]
            print(vocabulary)
            find_matches(vocabulary, matches)
            print(matches)
    else:
        print("Bad input. Exiting.")


if __name__ == '__main__':
    main()
