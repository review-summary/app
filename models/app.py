from flask import Flask, request, jsonify
from selectorlib import Extractor
import requests
from dateutil import parser as dateparser
from time import sleep
import random
from tfidf_model.tfidf import tfidf_sum

app = Flask(__name__)
e = Extractor.from_yaml_file('models/selectors.yml')
root_url = 'https://www.amazon.com'
reviews = []
histogram = {}
output = {}

model = tfidf_sum()

def main(url,flag):
    count = 0
    review_count = 0

    next_url = url

    while flag == 0:

        next_url = next_url + '&pageSize=20'
        result = scrape(next_url)

        if result['reviews'] == None: 
            print('Trouble with extractor (selectorlib) reading')
            output['reviews'] = reviews
            output['error'] = 'Trouble reading'
            return output

        if count == 0:
            for h in result['histogram']:
                if h['value'] != None:
                    histogram[h['key']] = h['value']

            output['histogram'] = histogram
            output['average_rating'] = float(result['average_rating'].split(' out')[0])
            output['number_of_ratings'] = int(result['number_of_reviews'].replace(",", "").split('  customer')[0])

        for r in result['reviews']:
            r["product"] = result["product_title"]
            r['url'] = url
            if 'verified_purchase' in r and r.get('verified'):
                if 'Verified Purchase' in r['verified_purchase']:
                    r['verified_purchase'] = True
                else:
                    r['verified_purchase'] = False
            r['rating'] = r['rating'].split(' out of')[0]
            date_posted = r['date'].split('on ')[-1]
            if r['images']:
                r['images'] = "\n".join(r['images'])
            r['date'] = dateparser.parse(date_posted).strftime('%d %b %Y')
            reviews.append(r)
            review_count += 1
        
        print ("Total number of reviews added:", review_count)

        next_url = root_url + result['next_page'] if result['next_page'] else root_url

        count += 1
        
        result.clear

        if next_url == root_url: flag = 1

    output['number_of_reviews'] = review_count
    output['reviews'] = reviews
    return output

def scrape(url):    

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None

    sleep_time = random.randrange(2, 5)
    print ("Sleep time is set to:", sleep_time)
    sleep(sleep_time)
    # Pass the HTML of the page and create
    return e.extract(r.text)

# @app.route('/')
# def api():
#     url = request.args.get('url',None)
#     if url:
#         data = main(url,0)
#         return jsonify(data)
#     return jsonify({'error':'URL to scrape is not provided'}),400

@app.route('/')
def show():
    url = request.args.get('url',None)
    if url:
        data = main(url,0)
    else:
        data = {}
    print(data)
    reviews, raw_reviews = model.process_reviews(data)
    tfidf_ratings = model.tfidf(reviews)
    summary, original_review = model.summarize_reviews(reviews, tfidf_ratings, raw_reviews)
    result = {}
    for i, sum in enumerate(summary):
        result[sum] = original_review[i]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)





# @app.route('/', methods = ['GET', 'POST'])
# def echo():
#     if request.method == 'GET':
#         data = request.args
#     else:
#         data = request.get_json()
#     return jsonify(data)


#     # return "Summarized Review is {} '\n' Original Review is {}".format(summary, original_review)

# if __name__=="__main__":
#     app.run(host='0.0.0.0', debug=True)
