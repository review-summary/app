import os
import json
import pandas as pd
import numpy as np
from operator import itemgetter
import gensim
from gensim import corpora, models

from preprocessing import token_lemmatize, lemmatize_stemming, bow
from utils import *


def lda_model(bow_corpus, dictionary):
    print("Running LDA model...")
    lda_model = gensim.models.LdaMulticore(bow_corpus,
                                       num_topics=2,
                                       id2word=dictionary, 
                                       passes=50,
                                       minimum_probability=0.02,
                                       random_state=41)
    return lda_model
# Save Model

# Load Model
# def review_2_topic(lda_model, bow_corpus):
# # Classify all docs into their topics
# # doc_topics = lda_model.get_document_topics(bow=bow_corpus[3], minimum_probability=None, minimum_phi_value=None, per_word_topics=False)

#     reviews2topics = {}
#     for i in range(len(bow_corpus)):    
#         review_topic = lda_model.get_document_topics(bow=bow_corpus[i], minimum_probability=None, minimum_phi_value=None, per_word_topics=False)
#         reviews2topics[i] = max(review_topic,key=itemgetter(1))[0]

#     topic_review_df = documents.copy()
#     topic_review_df['topic'] = pd.Series(reviews2topics)

#     #Dedupe
#     dedupe_topic_review_df = topic_review_df.drop_duplicates(['reviewText', 'overall', 'vote'])
#     return dedupe_topic_review_df

