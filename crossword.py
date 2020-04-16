"""
Filename: crossword.py
Purpose: Generates a crossword puzzle from given word:definition combinations.
Author: I.C.
Date: 15.4.2020
"""

import os
import sys
import re
import random

BOARD = [['.', '.', '.', '.', '.', chr(1487), '.', '.', '.', '.', '.', '.', '.'],
         ['.', chr(1487), '.', chr(1487), '.', chr(1487), '.', chr(1487), '.', chr(1487), '.', chr(1487), '.'],
         ['.', '.', '.', '.', '.', '.', '.', chr(1487), '.', '.', '.', '.', '.'],
         ['.', chr(1487), '.', chr(1487), '.', chr(1487), '.', chr(1487), '.', chr(1487), chr(1487), chr(1487), '.'],
         ['.', '.', '.', chr(1487), '.', '.', '.', '.', '.', '.', '.', '.', chr(1487)],
         ['.', chr(1487), '.', chr(1487), chr(1487), chr(1487), '.', chr(1487), '.', chr(1487), '.', chr(1487), '.'],
         ['.', '.', '.', '.', '.', '.', chr(1487), '.', '.', '.', '.', '.', '.'],
         ['.', chr(1487), '.', chr(1487), '.', chr(1487), '.', chr(1487), chr(1487), chr(1487), '.', chr(1487), '.'],
         [chr(1487), '.', '.', '.', '.', '.', '.', '.', '.', chr(1487), '.', '.', '.'],
         ['.', chr(1487), chr(1487), chr(1487), '.', chr(1487), '.', chr(1487), '.', chr(1487), '.', chr(1487), '.'],
         ['.', '.', '.', '.', '.', chr(1487), '.', '.', '.', '.', '.', '.', '.'],
         ['.', chr(1487), '.', chr(1487), '.', chr(1487), '.', chr(1487), '.', chr(1487), '.', chr(1487), '.'],
         ['.', '.', '.', '.', '.', '.', '.', chr(1487), '.', '.', '.', '.', '.']]

VERTICAL = 0
HORIZONTAL = 1

ORDER = [(0, 12, HORIZONTAL, 7, 1),  # 1h
         (0, 12, VERTICAL, 4, 1),  # 1v
         (0, 10, VERTICAL, 3, 2),  # 2v
         (2, 12, HORIZONTAL, 5, 8),  # 8h
         (0, 8, VERTICAL, 7, 3),  # 3v
         (0, 6, VERTICAL, 6, 4),  # 4v
         (4, 11, HORIZONTAL, 8, 10),  # 10h
         (0, 4, VERTICAL, 5, 5),  # 5v
         (2, 6, HORIZONTAL, 7, 9),  # 9h
         (0, 4, HORIZONTAL, 5, 5),  # 5h
         (0, 2, VERTICAL, 9, 6),  # 6v
         (0, 0, VERTICAL, 8, 7),  # 7v
         (4, 2, HORIZONTAL, 3, 12),  # 12h
         (6, 5, HORIZONTAL, 6, 15),  # 15h
         (8, 8, HORIZONTAL, 8, 19),  # 19h
         (6, 4, VERTICAL, 7, 16),  # 16v
         (7, 6, VERTICAL, 6, 17),  # 17v
         (12, 6, HORIZONTAL, 7, 25),  # 25h
         (10, 4, HORIZONTAL, 5, 22),  # 22h
         (10, 2, VERTICAL, 3, 23),  # 23v
         (9, 0, VERTICAL, 4, 20),  # 20v
         (8, 8, VERTICAL, 5, 19),  # 19v
         (10, 12, HORIZONTAL, 7, 21),  # 21h
         (4, 10, VERTICAL, 9, 11),  # 11v
         (6, 12, HORIZONTAL, 6, 14),  # 14h
         (12, 12, HORIZONTAL, 5, 24),  # 24h
         (5, 12, VERTICAL, 8, 13),  # 13v
         (8, 12, HORIZONTAL, 3, 18)  # 18h
         ]


def get_word_def_dict(filename):
    """
    Extracts the words and their definitions from crossword data file.
    :param filename: The path to the crossword data
    :return: A dict containing words as keys and definitions as their values.
    """
    with open(filename, 'r') as file:
        return {line.rstrip().split('-')[0]: line.rstrip().split('-')[1] for line in file}


def get_order_from_board(board):
    """
    Gets an order list (list of tuples with row, col, direction(h/v), length, and number (for definitions) from board. Interpret the blank spaces.
    :param board: The board to create and order for.
    :return: A list containing the order for the recursion to explore the board.
    """
    pass


def get_board_slot(order_entry, board):
    """
    Gets the current state of a slot in the board.
    :param order_entry: The place in the board to look at.
    :param board: The board to get slot from.
    :return: A string of the slot e.g. "B.n.na"
    """
    y, x, direction, length, number = order_entry
    if direction == HORIZONTAL:
        characters = board[y][x - length + 1:x + 1]
        characters.reverse()
    else:
        characters = [row[x] for row in board][y: y + length]

    return ''.join(characters)


def find_matches_in_data(string_to_match, word_def_dict):
    """
    Finds words in the crossword data that match a given string from a slot.
    :param string_to_match: The string from the board we are looking to match.
    :param word_def_dict: The dict of words and definitions to look at words.
    :return: A list of possible words, or None if there aren't any.
    """
    regex_expression = re.compile('\\b' + string_to_match + '\\b')
    return list(filter(regex_expression.search, word_def_dict.keys()))


def insert_match_into_board(board, order_entry, matching_word):
    """
    Inserts a string into the board at given location.
    :param board: The board to insert into.
    :param order_entry: The place to insert at.
    :param matching_word: The word to insert.
    :return: None, is applied directly to the global board.
    """
    y, x, direction, length, number = order_entry

    if direction == HORIZONTAL:
        board[y][x - length + 1:x + 1] = ''.join(reversed(matching_word))
    else:
        for row in range(y, y + length):
            board[row][x] = matching_word[row - y]


def print_board(board):
    """
    Better printing of the playing board.
    :param board: The board to print.
    """
    print('_ ' * 15)
    for s in board:
        print('|', ' '.join(reversed(s)), '|')
    print('_ ' * 15)


def print_definitions(order, word_def_dict, board):
    """
    Prints the definitions according to the place in the board.
    :param order: The order according to which words were placed.
    :param word_def_dict: The words and definitions pairing dict.
    :param board: The board to print definitions for words in.
    """
    print("מאוזן")
    for order_entry in order:
        y, x, direction, length, number = order_entry
        if direction == HORIZONTAL:
            print(str(number) + '.', word_def_dict[get_board_slot(order_entry, board)])
    print("מאונך")
    for order_entry in order:
        y, x, direction, length, number = order_entry
        if direction == VERTICAL:
            print(str(number) + '.', word_def_dict[get_board_slot(order_entry, board)])


def generate_by_template(board, order, word_def_dict):
    """
    Main board generation function.
    :param board: The board to generate filling for.
    :param order: The order in which to generate (minimizes time the better the order is).
    :param word_def_dict: The words and definitions to fill with.
    :return: None, merely for recursion purposes.
    """
    for order_entry in order:
        string_to_match = get_board_slot(order_entry, board)
        print(string_to_match)
        matching_words = find_matches_in_data(string_to_match, word_def_dict)
        random.shuffle(matching_words)
        print(matching_words)
        for word in matching_words:
            print(word)
            insert_match_into_board(board, order_entry, word)
            removed_word_def_dict = word_def_dict.copy()
            removed_word_def_dict.pop(word, None)
            print_board(board)
            generate_by_template(board, order[1:], removed_word_def_dict)
            print(word, "we left on")
            if '.' not in (item for sublist in board for item in sublist):
                print_board(board)
                print_definitions(ORDER, get_word_def_dict("crossword_data.txt"), board)
                sys.exit(1)
            else:
                insert_match_into_board(board, order_entry, string_to_match)

        return


def generate_freestyle(word_def_dict):
    """
    Generate a freestyle crossword, one not in the shape of a square.
    *In the works.
    :param word_def_dict: The word-definition dict for the crossword puzzle.
    :return: None.
    """
    pass


def main():
    # Data is in crossword_data.txt.
    if len(sys.argv) != 3:
        print('usage: ./crossword.py {--bytemplate | --freestyle} file')
        sys.exit(1)

    option = sys.argv[1]
    filename = sys.argv[2]
    board = BOARD
    order = ORDER
    word_def_dict = get_word_def_dict(filename)

    if option == '--bytemplate':
        generate_by_template(board, order, word_def_dict)
    elif option == '--freestyle':
        generate_freestyle(word_def_dict)
    else:
        print('unknown option: ' + option)
        sys.exit(1)



if __name__ == '__main__':
    main()
