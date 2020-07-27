import re
import random
from typing import List


def split_to_sentences(text: str, min_length: int = 10) -> List[str]:
    # to find n-th sentence without preprocessing
    text = re.sub(r'([!?\.])+', r'\1[[SEP]]', text)
    output = []
    for sentence in text.split('[[SEP]]'):
        sentence = sentence.strip()
        if len(sentence) >= min_length:
            output.append(sentence)
    return output


def preprocess(documents: List[dict]) -> List[dict]:
    return [doc['reviewText'] for doc in documents]


def predict(documents: List[str], num_sentences: int = 5) -> List[dict]:
    return random.sample(
        [random.sample(split_to_sentences(doc), 1) for doc in documents],
        num_sentences
    )  # type: ignore
