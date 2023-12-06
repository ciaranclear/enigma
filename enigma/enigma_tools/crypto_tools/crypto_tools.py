import re


BIGRAMS = [
        "th","he","in",
        "er","an","re",
        "on","at","en",
        "nd","ti","es",
        "or","te","of",
        "ed","is","it",
        "al","ar","st",
        "to","nt","ng",
        "se","ha","as",
        "ou","io","le",
        "ve","co","me",
        "de","hi","ri",
        "ro","ic","ne",
        "ea","ra","ce"
    ]

TRIGRAMS = [
        "the","and",
        "tha","ent",
        "ing","ion",
        "tio","for",
        "nde","has",
        "nce","edt",
        "tis","oft",
        "sth","men"
    ]


def bigram_count(text):
    """
    Returns two items. The first item is a dictionary with a key value
    pair of each bigram found and number of occurences. The second item
    returned is the total number of bigrams found.
    """
    bigrams = {}
    count = 0

    for bigram in BIGRAMS:
        pattern = re.compile(bigram, re.IGNORECASE)
        matches = list(pattern.finditer(text))
        if matches:
            count += len(matches)
            bigrams[bigram] = len(matches)
    return bigrams, count

def trigram_count(text):
    """
    Returns two items. The first item is a dictionary with a key value
    pair of each trigram found and number of occurences. The second item
    returned is the total number of trigrams found.
    """
    trigrams = {}
    count = 0

    for trigram in TRIGRAMS:
        pattern = re.compile(trigram, re.IGNORECASE)
        matches = list(pattern.finditer(text))
        if matches:
            count += len(matches)
            trigrams[trigram] = len(matches)
    return trigrams, count

def index_of_coincidence(text):

    chars = [chr(i) for i in range(65, 91)]

    count = 0

    ioc = 0
        
    d = {c:{"number":0, "ioc":0.0} for c in chars}

    for char in text:
        char = char.upper()
        if char in chars:
            count += 1
            d[char]["number"] += 1

    for char in d:
        n = d[char]["number"]
        if n > 1:
            _ioc = (n/count)*((n-1)/(count-1))
        else:
            _ioc = 0
        d[char]["ioc"] = _ioc
        ioc += _ioc
        
    normalized_ioc = ioc * 26

    return count, ioc, normalized_ioc