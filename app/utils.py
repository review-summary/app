# This utils module is for temporarily reading and processing json data for demo purposes, delete this module once it is productionized

def load_data(file_path):
    data = []
    with gzip.open(file_path) as f:
        for l in f:
            data.append(json.loads(l.strip()))
    df = pd.DataFrame.from_dict(data)
    core_data = extract_core_cols(df)
    return core_data

def extract_core_cols(data):
    data_text = data[['reviewText']]

    data_text.loc[:,'index'] = data_text.index
    data_text.loc[:,'vote'] = data['vote']
    data_text.loc[:,'asin'] = data['asin']
    data_text.loc[:,'overall'] = data['overall']
    return data_text

def rating_filter(documents, rating):
    return documents[documents['overall']==rating][['reviewText', 'vote', 'asin', 'overall']].reset_index(drop=True)

def rating_splitter(core_data, product_id, rating_range=range(1,6)):
    documents = core_data[core_data['asin']==product_id].copy()
    documents_all_rating = {}
    for rating in rating_range:
        document_single_rating = rating_filter(documents, rating)
        documents_all_rating[rating] = document_single_rating
    return documents_all_rating
    