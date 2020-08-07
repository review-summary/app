from sentence_transformers import SentenceTransformer

def bert_model(product_name):
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    data = load_data("app/sample_reviews.json", product_name)
    corpus = data['reviewText'].to_list()
    corpus_embeddings = embedder.encode(corpus)
    return corpus_embeddings