from models.tfidf import preprocess


def test_preprocess():
    reviews = [
        {'reviewText': "This is first sentence of first review. This is second sentence of first review."},
        {'reviewText': "This is first sentence of second review. This is second sentence of second review."}
    ]
    review_sentences, review_words = preprocess(reviews)
    
    assert review_sentences[0] == [
        "This is first sentence of first review", "This is second sentence of first review"]
    assert review_sentences[1] == [
        "This is first sentence of second review", "This is second sentence of second review"]
    assert review_words[0] == [
        ["this", "is", "first", "sentence", "of", "first", "review"],
        ["this", "is", "second", "sentence", "of", "first", "review"]
    ]
    assert review_words[1] == [
        ["this", "is", "first", "sentence", "of", "second", "review"],
        ["this", "is", "second", "sentence", "of", "second", "review"]
    ]