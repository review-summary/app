import random
from preprocessing import extract_sentences


def predict(reviews, num_sentences = 5):
    documents = [
        random.sample(extract_sentences(review['reviewText']), 1)[0] for review in reviews
    ]
    return random.sample(documents, num_sentences)
