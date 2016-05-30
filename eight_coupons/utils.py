"""
.. module:: utils.py

Text processing utils
"""
import re
import snowballstemmer
from bs4 import BeautifulSoup


# A regexp to split the words by
splitter = re.compile(r"[\s\.-]")


stemmer = snowballstemmer.stemmer("english")


def split_stems(str):
    """
    Extracts all stems from given string, ripping off any HTML tags

    :param: str
      A string to extract stems from

    TODO: Check for incorrect HTML
    """
    content = ''.join(BeautifulSoup(str, "html.parser").findAll(text=True))
    for word in splitter.split(content):
        if not word:
            continue
        word = word.lower()
        yield stemmer.stemWord(word)
