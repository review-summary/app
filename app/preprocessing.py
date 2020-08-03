import re
import gensim
import nltk
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np

def clean(text):
    text = text.lower()
    text = re.sub(r"'", '', text)
    text = re.sub(r'[^a-z0-9?.!]', ' ', text)    # only alnum & interpunction
    text = re.sub(r'([a-z]+)' , r' \1 ', text)   # add spaces before & after words
    text = re.sub(r'([^\w\s])\1+', r'\1', text)  # remove repeated chars
    text = re.sub(r'\d+', 'NUM', text)           # replace numbers with tokens
    text = re.sub(r'\s+', ' ', text)             # remove extra spaces
    return text


def extract_words(sentences):
    return [sentence.strip().split(' ') for sentence in sentences if sentence != '']


def split_sentences(text):
    return re.sub(r'(\s*[.?!\n]\s*)', 'SEP', text).split('SEP')


def extract_sentences(text, min_length = 10):
    sentences = split_sentences(text)
    return [sentence for sentence in sentences if len(sentence) >= min_length]

def lemmatize_stemming(text):
    # nltk.download('wordnet')
    stemmer = SnowballStemmer("english")
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

# Tokenize and lemmatize
def token_lemmatize(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

def bow(processed_docs):
    dictionary = gensim.corpora.Dictionary(processed_docs)
    bow_corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in processed_docs]
    return bow_corpus

 
