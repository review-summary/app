from flask import Flask, jsonify, request, render_template, redirect, url_for
from models.arbitrary import predict

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    data = request.get_json()
    return jsonify(predict(data))


@app.route('/form', methods=['GET', 'POST'])
def form():
    products = [
        "Disney Mickey Mouse Deluxe Boys' Costume",
        "Levi's Men's 501 Original Fit Jeans, Polished Black, 44W x 30L",
        "Levi's Men's 501 Original-Fit Jeans, Trashed, 33W x 32L",
        "Hanes Absolutely Ultra Sheer Sheer Control Top SF (Single) Size:E Color:Jet",
        "Merrell Women's Jungle Moc Taupe Slip-On Shoe - 8.5 B(M) US",
        "sofsy Soft-Touch Rayon Blend Tie Front Nursing & Maternity Fashion Top Charcoal Small",
        "The Last Life: A Novel",
    ]
    if request.method == 'POST':
        selected = request.form.get("products")
        print(selected)
    else:
        selected = ""
    return render_template('form.html', products=products, selected=selected)


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
