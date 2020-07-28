import math
import random
from collections import Counter
import numpy as np
from preprocessing import clean, extract_words, extract_sentences


def preprocess(reviews):
    review_sentences = [extract_sentences(review['reviewText']) for review in reviews]
    review_words = []
    
    for sentences in review_sentences:
        sentence_words = []
        for sentence in sentences:
            sentence = clean(sentence)
            sentence = extract_words(sentence)
            sentence_words.append(sentence)
        review_words.append(sentence_words)
    
    return review_sentences, review_words


def predict(reviews, num_sentences = 5):
    review_sentences, review_words = preprocess(reviews)
    review_tfidf = assign_tfidf_scores(review_words)
    assert len(review_sentences) == len(review_words) == len(review_tfidf)
    
    best_sentences = []
    for i in range(len(review_sentences)):
        sentence_ratings = []
        for sentence in review_words[i]:
            best = 0
            for word in sentence:
                best = max(best, review_tfidf[i][word])
            sentence_ratings.append(best)
        idx = np.argmax(sentence_ratings)
        best_sentences.append(review_sentences[i][idx])

    return random.sample(best_sentences, num_sentences)


def assign_tfidf_scores(documents):
    # standard TF-IDF, as in https://en.wikipedia.org/wiki/Tf%E2%80%93idf
    
    N = len(documents)
    df = Counter()
    tfs = []

    for document in documents:
        f = Counter()
        words = set()

        for sentence in document:
            for word in sentence:
                f[word] += 1
                words.add(word)

        f = dict(f)
        c = max(f.values())
        tfs.append({k: v/c for k, v in f.items()})

        for word in words:
            df[word] += 1
    
    idf = {k: math.log(N / v) for k, v in dict(df).items()}

    result = []
    for tf in tfs:
        tfidf = {}
        for k, v in tf.items():
            tfidf[k] = v * idf[k]
        result.append(tfidf)
    return result
