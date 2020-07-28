import math
from collections import Counter
import re
import numpy as np
from tfidf_model.config import *
from tfidf_model.utils import *
print(PATH)

class tfidf_sum():
    def __init__(self):
        self.path = PATH
        self.asin = asin

    def list_product(self, path):
        products = set()
        review_count = 0

        for review in parse(self.path):
            review_count += 1
            products.add(review['asin'])
        return products

    # review_count, len(products), review_count / len(products)
    def process_reviews(self, path, asin):

        raw_reviews = []

        for review in parse(self.path):
            print(review)
            if review['asin'] == self.asin:
                raw_reviews.append(review)
            elif len(raw_reviews) > 0:
                # assuming that they're ordered
                break

        reviews = []
        for review in raw_reviews:
            if review['asin'] == self.asin:
                reviews.append(preprocess(review['reviewText']))
            
        return reviews, raw_reviews

    def tfidf(self, documents):
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

    def split_to_sentences(self, text):
        # to find n-th sentence without preprocessing
        text = re.sub(r'([!?\.])+', r'\1[[SEP]]', text)
        return [sentence.strip() for sentence in text.split('[[SEP]]')]


    def summarize_reviews(self, reviews, tfidf_ratings, raw_reviews):
        summaries = []
        original_reviews = []
        for review, ratings, raw in zip(reviews, tfidf_ratings, raw_reviews):
            avg_sentence_ratings = [] 
            for sentence in review:
                high = 0
                for word in sentence:
                    high = max(high, ratings[word])  # max seemed to work slightly better than mean 
                avg_sentence_ratings.append(high)
            idx = np.argmax(avg_sentence_ratings)
            
            summary= self.split_to_sentences(raw['reviewText'])[idx]
            original_review = re.sub(r'[\t\n ]+', ' ', raw['reviewText'])
            summaries.append(summary)
            original_reviews.append(original_review)

            print('Summazrised Review:', self.split_to_sentences(raw['reviewText'])[idx])
            print(re.sub(r'[\t\n ]+', ' ', raw['reviewText']))
            print('\n')
        return summaries, original_reviews