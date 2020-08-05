import os
import json
import pandas as pd
import numpy as np
from operator import itemgetter
import gensim
from gensim import corpora, models
from sklearn.cluster import KMeans

from preprocessing import token_lemmatize, lemmatize_stemming, bow
from utils import *

gamma = 10
AE = None

def lda_model(bow_corpus, dictionary, fname, k=2):
    print("Training LDA model...")
    lda_model = gensim.models.LdaMulticore(bow_corpus,
                                       num_topics=k,
                                       id2word=dictionary, 
                                       passes=50,
                                       minimum_probability=0.02,
                                       random_state=41)
    # Save Model
    lda_model.save("app/models/saved_models/lda/" + fname)
    return lda_model

def get_vec_lda(model, corpus, k=2):
    """
    Get the LDA vector representation (probabilistic topic assignments for all documents)
    :return: vec_lda with dimension: (n_doc * n_topic)
    """
    n_doc = len(corpus)
    vec_lda = np.zeros((n_doc, k))
    for i in range(n_doc):
        # get the distribution for the i-th document in corpus
        for topic, prob in model.get_document_topics(corpus[i]):
            vec_lda[i, topic] = prob

    return vec_lda

# Load Model
def load_lda_model(fname):
    model =  gensim.models.LdaMulticore.load(fname)
    return model

def bert_encode(sentences):
    print('Getting vector representations for BERT ...')
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('bert-base-nli-max-tokens')
    vec = np.array(model.encode(sentences, show_progress_bar=True))

def lda_bert(model, corpus, sentences, gamma)
    vec = {}
    vec_lda = get_vec_lda(model, corpus, k=2)
    vec_bert = bert_encode(sentences)
    vec_ldabert = np.c_[vec_lda * gamma, vec_bert]
    vec['LDA_BERT_FULL'] = vec_ldabert
    if not AE:
        AE = Autoencoder()
        print('Fitting Autoencoder ...')
        AE.fit(vec_ldabert)
        print('Fitting Autoencoder Done!')
    vec = AE.encoder.predict(vec_ldabert)
    return vec

def clustering(corpus_embeddings, num_clusters = 5):
    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_
    return cluster_assignment