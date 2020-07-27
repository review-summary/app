import math
from collections import Counter
import re
import numpy as np
from config import *
from utils import *

def list_product(PATH):
    products = set()
    review_count = 0

    for review in parse(PATH):
        review_count += 1
        products.add(review['asin'])
    return products

# review_count, len(products), review_count / len(products)
def process_reviews(PATH, asin):

    raw_reviews = []

    for review in parse(PATH):
        print(review)
        if review['asin'] == asin:
            raw_reviews.append(review)
        elif len(raw_reviews) > 0:
            # assuming that they're ordered
            break

    reviews = []
    for review in raw_reviews:
        if review['asin'] == asin:
            reviews.append(preprocess(review['reviewText']))
        
    return reviews, raw_reviews

def tfidf(documents):
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
        doc_tfidf = {}
        for k, v in tf.items():
            doc_tfidf[k] = v * idf[k]
        result.append(doc_tfidf)
    return result

def split_to_sentences(text):
    # to find n-th sentence without preprocessing
    text = re.sub(r'([!?\.])+', r'\1[[SEP]]', text)
    return [sentence.strip() for sentence in text.split('[[SEP]]')]


reviews, raw_reviews = process_reviews(PATH, asin)
tfidf_ratings = tfidf(reviews)



for review, ratings, raw in zip(reviews, tfidf_ratings, raw_reviews):
    avg_sentence_ratings = [] 
    for sentence in review:
        high = 0
        for word in sentence:
            high = max(high, ratings[word])  # max seemed to work slightly better than mean 
        avg_sentence_ratings.append(high)
    idx = np.argmax(avg_sentence_ratings)

    print('Summazrised Review:', split_to_sentences(raw['reviewText'])[idx])
    print(re.sub(r'[\t\n ]+', ' ', raw['reviewText']))
    print('\n')