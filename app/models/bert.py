from sentence_transformers import SentenceTransformer
from utils import * 

def bert_model(product_name):
    embedder = SentenceTransformer('bert-base-nli-mean-tokens')

    print("Processing Reviews...")
    ratings_documents, raw_data = read_split('app/sample_reviews.json', product_name)
    documents_rating_1 = ratings_documents[1]
    documents_rating_5 = ratings_documents[5]
    corpus_1 = documents_rating_1['reviewText'].to_list()
    corpus_5 = documents_rating_5['reviewText'].to_list()
    corpus_embeddings_1 = embedder.encode(corpus_1)
    corpus_embeddings_5 = embedder.encode(corpus_5)
    return corpus_embeddings_1, corpus_embeddings_5, raw_data['reviewText'].to_list()