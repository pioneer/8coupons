import re
import snowballstemmer
from bs4 import BeautifulSoup


splitter = re.compile(r"[\s\.-]")


stemmer = snowballstemmer.stemmer("english")


def split_stems(s):
    # TODO: Check for incorrect HTML
    content = ''.join(BeautifulSoup(s).findAll(text=True))
    for word in splitter.split(content):
        if not word:
            continue
        word = word.lower()
        yield stemmer.stemWord(word)
