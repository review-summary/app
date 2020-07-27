import gzip
import json
import re
from tfidf_model.config import *

def parse(path):
    # g = gzip.open(path, 'r')
    reviewsList = []
    # with open(path) as json_file:
    #     for l in json_file:
    #         yield json.loads(l)
    # with open(path) as f:
    #     for jsonObj in f:
    #         reviewDict = json.loads(jsonObj)
    #         reviewsList.append(reviewDict)
    with open(path, 'r') as reviews:
        review_data = reviews.read()
    
    obj = json.loads(review_data)
    return obj


def take_n(n):
    fields = ['asin', 'overall', 'summary', 'reviewText']
    raw = []
    for i, review in enumerate(parse(PATH)):
        raw.append({k: v for k,v in review.items() if k in fields})
        if i > n:
            break
    return raw

def clean(text):
    text = text.lower()
    text = re.sub(r"'", '', text)
    text = re.sub(r'[^a-z0-9?.!]', ' ', text)    # only alnum & interpunction
    text = re.sub(r'([a-z]+)' , r' \1 ', text)   # add spaces before & after words
    text = re.sub(r'([^\w\s])\1+', r'\1', text)  # remove repeated chars
    text = re.sub(r'\d+', 'NUM', text)           # replace numbers with tokens
    text = re.sub(r'\s+', ' ', text)             # remove extra spaces
    return text

def split_sentences(text):
    return re.sub(r'([.?!])', r'SEP', text).split('SEP')

def extract_words(text):
    return [sentence.strip().split(' ') for sentence in text if sentence != '']

def preprocess(text):
    text = clean(text)
    text = split_sentences(text)
    text = extract_words(text)
    return text

# for review in take_n(5):
#     print(preprocess(review['reviewText']))

