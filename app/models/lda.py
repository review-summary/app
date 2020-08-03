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


