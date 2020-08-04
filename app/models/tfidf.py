import math
from collections import Counter
from preprocessing import clean, extract_words


def preprocessed(documents):
    for document in documents:
        document = clean(document)
        document = extract_words(document)
        yield document


def tfidf_encode(documents):
    """TF-IDF encoder

    >>> import re
    >>> corpus = [
        'This is the first document.',
        'This document is the second document.',
        'And this is the third one.',
        'Is this the first document?',
    ]
    >>> documents = [document for document in preprocessed(corpus)]
    >>> tfidf_encode(documents)
    [[0.0, 0.0, 0.0, 0.6931471805599453, 0.0, 0.28768207245178085],
     [0.0, 0.0, 0.0, 0.0, 0.6931471805599453, 0.0, 0.14384103622589042],
     [1.3862943611198906,
     0.0,
     0.0,
     0.0,
     1.3862943611198906,
     1.3862943611198906,
     0.28768207245178085],
     [0.0, 0.0, 0.0, 0.6931471805599453, 0.0, 1.3862943611198906]]

    """
    # standard TF-IDF, as in https://en.wikipedia.org/wiki/Tf%E2%80%93idf

    N = len(documents)
    df = Counter()
    tf = []

    for document in documents:
        f = Counter()
        for word in document:
            f[word] += 1
            df[word] += 1
        f = dict(f)
        c = max(f.values())
        tf.append({k: v/c for k, v in f.items()})

    idf = {k: math.log(N / v) for k, v in df.items()}

    scores = []
    for i, document in enumerate(documents):
        encoded_document = []
        for word in document:
            encoded_document.append(tf[i][word] * idf[word])
        scores.append(encoded_document)

    return scores
