"""
Filename: word_creation_algorithms.py
Purpose: Creates definitions for words with jumbles, surrounds and concatenations of other Hebrew words.
Author: I.C.
Date: 15.4.2020
"""

from itertools import permutations


def jumble(vocabulary, word, matches):
    """

    :param vocabulary:
    :param word:
    :param matches:
    :return:
    """
    perms = set([''.join(p) for p in permutations(word)])
    for permutation in perms:
        for index in range(len(word)):
            start, end = permutation[:index], permutation[index:]
            if start in vocabulary and end in vocabulary:
                key = word, "ערבוב"
                if sorted([start, end]) not in (matches.get(word, "הלחם"), []) \
                        and sorted([start, end]) not in (matches.get(word, "היקף"), []):
                    if key not in matches.keys():
                        matches[key] = [sorted([start, end])]
                    elif sorted([start, end]) not in matches.get(key):
                        matches[key].append(sorted([start, end]))


def concatenate(vocabulary, word, first_index, matches):
    """

    :param vocabulary:
    :param word:
    :param first_index:
    :param matches:
    :return:
    """
    start, end = word[:first_index], word[first_index:]
    if start in vocabulary and end in vocabulary:
        key = word, "הלחם"
        if key not in matches.keys():
            matches[key] = [sorted([start, end])]
        elif sorted([start, end]) not in matches.get(key):
            matches[key].append(sorted([start, end]))


def surround(vocabulary, word, first_index, second_index, matches):
    """

    :param vocabulary:
    :param word:
    :param first_index:
    :param second_index:
    :param matches:
    :return:
    """
    start, middle, end = word[:first_index], word[first_index:second_index], word[second_index:]
    if start + end in vocabulary and middle in vocabulary:
        key = word, "היקף"
        if key not in matches.keys():
            matches[key] = [sorted([start + end, middle])]
        elif sorted([start + end, middle]) not in matches.get(key):
            matches[key].append(sorted([start + end, middle]))


def find_matches(vocabulary, matches):
    """

    :param vocabulary:
    :param matches:
    :return:
    """
    for word in vocabulary:
        # First split
        for first_index in range(2, len(word)):
            # Second split - Surrounding definition
            for second_index in range(first_index + 2, len(word) - 1):
                surround(vocabulary, word, first_index, second_index, matches)

            # Concat-ing definition
            concatenate(vocabulary, word, first_index, matches)

        # Permutations and then splitting - jumbling definition
        jumble(vocabulary, word, matches)
