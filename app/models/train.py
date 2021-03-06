import gensim
from preprocessing import token_lemmatize, bow
from utils import read_split


def process_reviews(product_name):
    print("Processing Reviews...")
    ratings_documents = read_split('sample_reviews.json', product_name)
    documents_rating_1 = ratings_documents[1]
    documents_rating_5 = ratings_documents[5]

    bow_corpus_1, dictionary_1 = process_single_product_reviews(documents_rating_1)
    bow_corpus_5, dictionary_5 = process_single_product_reviews(documents_rating_5)
    return bow_corpus_1, dictionary_1, bow_corpus_5, dictionary_5, documents_rating_1, documents_rating_5


def process_single_product_reviews(documents):
    # Preprocess all reviews
    processed_docs = documents['reviewText'].map(token_lemmatize)

    # BOG
    dictionary = gensim.corpora.Dictionary(processed_docs)

    bow_corpus = bow(processed_docs)

    # tfidf = models.TfidfModel(bow_corpus)
    # corpus_tfidf = tfidf[bow_corpus]
    return bow_corpus, dictionary

