# This utils module is for temporarily reading and processing json data for demo purposes, delete this module once it is productionized
import gzip
import json
import pandas as pd
import numpy as np
from operator import itemgetter

def load_data(file_path, product_name=None):
    """
    Purpose: load json data from the sample file, regardless of how many products are
    in the file, concatenate them into a single dataframe for further processing.
    """
    with open(file_path) as f:
        data = json.load(open(file_path))
    prod_revs = data[product_name]
    df = pd.DataFrame.from_dict(prod_revs)
    df = df.dropna(subset=['reviewText'])
    return df

# def dict_to_df(reviews, i):
#     df = pd.DataFrame.from_dict(list(reviews.values())[i])
#     df['productName'] = list(data.keys())[i]
#     return df

# def get_all_prod_revs(data):
#     frames = [ dict_to_df(data, i) for i in range(len(data)) ]
#     result = pd.concat(frames)
#     return result

def extract_core_cols(data):
    data_text = data[['reviewText']]

    data_text.loc[:,'index'] = data_text.index
    data_text.loc[:,'vote'] = data['vote']
    data_text.loc[:,'asin'] = data['asin']
    data_text.loc[:,'overall'] = data['overall']
    return data_text

def rating_filter(documents, rating):
    return documents[documents['overall']==rating][['reviewText', 'vote', 'asin', 'overall']].reset_index(drop=True)

def rating_splitter(core_data, rating_range=list(range(1,6))):
#     documents = core_data[core_data['asin'].isin(product_id)].copy()
    documents_all_rating = {}
    for rating in rating_range:
        document_single_rating = rating_filter(core_data, rating)
        documents_all_rating[rating] = document_single_rating
    return documents_all_rating

def read_split(file_path, product_name=None):
    raw_data = load_data(file_path, product_name)
    return rating_splitter(raw_data), raw_data
