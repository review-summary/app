import random
import re
from gensim.summarization.summarizer import summarize
from preprocessing import extract_sentences, lemmatize_stemming, token_lemmatize, bow, split_sentences
from models.lda import *
from models.train import *

def predict(reviews, num_sentences = 5):
    documents = [
        random.sample(extract_sentences(review['reviewText']), 1)[0] for review in reviews
    ]
    return random.sample(documents, num_sentences)

def run_model(product_name):
    bow_corpus_1, dictionary_1, bow_corpus_5, dictionary_5, documents_rating_1, documents_rating_5 = process_reviews(product_name)
    model_name_1 = re.sub("[ ,']", '_', product_name) + "_1_star.model"
    model_name_5 = re.sub("[ ,']", '_', product_name) + "_5_star.model"
    try:
        print("Loading LDA models...")
        model_1 = load_lda_model("app/models/saved_models/lda/" + model_name_1)
        model_5 = load_lda_model("app/models/saved_models/lda/" + model_name_5)
    except:
        model_1 = lda_model(bow_corpus_1, dictionary_1, model_name_1)
        model_5 = lda_model(bow_corpus_5, dictionary_5, model_name_5)
    return documents_rating_1, documents_rating_5, bow_corpus_1, bow_corpus_5, model_1, model_5

def review_2_topic(documents, lda_model, bow_corpus):
# Classify all docs into their topics

    reviews2topics = {}
    for i in range(len(bow_corpus)):    
        review_topic = lda_model.get_document_topics(bow=bow_corpus[i], minimum_probability=None, minimum_phi_value=None, per_word_topics=False)
        reviews2topics[i] = max(review_topic,key=itemgetter(1))[0]

    topic_review_df = documents.copy()
    topic_review_df['topic'] = pd.Series(reviews2topics)

    #Dedupe
    dedupe_topic_review_df = topic_review_df.drop_duplicates(['reviewText', 'overall', 'vote'])
    short_review_removed_topic_review_df = dedupe_topic_review_df[dedupe_topic_review_df['reviewText'].map(split_sentences).map(len)>1]
    # commented out summarize code as the function requires more than 1 sentence to work, even with the filter above set to len > 3, summarize does not always work...
    # Replace with tfidf or other summarizer
    # short_review_removed_topic_review_df['reviewText'] = short_review_removed_topic_review_df['reviewText'].apply(summarize, ratio=0.5)
    sorted_topic_review_df = short_review_removed_topic_review_df.sort_values(by=['vote'], ascending=False)
    sorted_topic_review_df = sorted_topic_review_df[sorted_topic_review_df['reviewText'].map(len)>1]
    return sorted_topic_review_df[sorted_topic_review_df['topic']==0], sorted_topic_review_df[sorted_topic_review_df['topic']==1]#, sorted_topic_review_df[sorted_topic_review_df['topic']==2]