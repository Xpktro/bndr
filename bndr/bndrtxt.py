# coding:utf-8

import random

import sys


def textbndr(text):
    result = text[:]
    result = ''.join(map(upper, result))
    result = ''.join(map(symbol_replace, result))
    return result


def upper(char):
    if random.choice((True, False, False, False)):
        return char.upper()
    return char


def symbol_replace(char):
    if char in ' -_.' and random.choice((True, False, False, False)):
        return random.choice(' -_.*!#+') + \
               (' ' if random.choice((True, False, False, False, False))
                else '')
    return char


def main():
    if len(sys.argv) > 1:
        print(textbndr(u' '.join(sys.argv[1:])))

if __name__ == '__main__':
    main()

