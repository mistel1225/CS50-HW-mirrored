from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    # TODO
    filea = set(a.split("\n"))
    fileb = set(b.split("\n"))
    return filea & fileb


def sentences(a, b):
    """Return sentences in both a and b"""

    # TODO
    filea = set(sent_tokenize(a))
    fileb = set(sent_tokenize(b))
    return filea & fileb

def substring_tokenize(str, n):
    substrings = []

    for i in range(len(str) - n + 1):
        substrings.append(str[i:i + n])

    return substrings
def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # TODO
    filea = set(substring_tokenize(a, n))
    fileb = set(substring_tokenize(b, n))
    return filea & fileb