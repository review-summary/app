from sentence_transformers import SentenceTransformer
from utils import read_split
import logging

log = logging.getLogger(__name__)

# we want this available on module load, not on first call
# if this loads on first call, than the first time user wants to use the app, there's a delay
bert = SentenceTransformer('bert-base-nli-mean-tokens')


def bert_model(product_name):
    log.info("Processing Reviews...")
    
    ratings_documents, raw_data = read_split('sample_reviews.json', product_name)
    documents_rating_1 = ratings_documents[1]
    documents_rating_5 = ratings_documents[5]
    corpus_1 = documents_rating_1['reviewText'].to_list()
    corpus_5 = documents_rating_5['reviewText'].to_list()
    corpus_embeddings_1 = bert.encode(corpus_1)
    corpus_embeddings_5 = bert.encode(corpus_5)
    
    return corpus_embeddings_1, corpus_embeddings_5, raw_data['reviewText'].to_list()
