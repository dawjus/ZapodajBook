import pandas as pd
from flask import Flask, request, jsonify
from gensim.models import KeyedVectors
from nltk import download
from nltk.corpus import stopwords

import find_book_service
from csv_parser import load_from_csv

app = Flask(__name__)

#Loading DatBase and Model
df = pd.read_csv('database/goodreads_data.csv')
matrix = load_from_csv('model/data.csv')
model = KeyedVectors.load_word2vec_format('model/GoogleNews-vectors-negative300-SLIM.bin', binary=True)
download('stopwords')
stop_words = stopwords.words('english')

@app.route('/')
def hello_world():
    return 'TU BEDZIE COS FAJNEGO'


@app.route('/book', methods=['POST'])
def find_book():
    data = request.get_json()
    book_title = data.get('title', '')
    result = find_book_service.find_book(book_title, df, matrix)
    return jsonify({'Books': result})


@app.route('/description', methods=['POST'])
def find_description():
    data = request.get_json()
    description = data.get('description', '')
    result = find_book_service.find_book_with_description(description, df, stop_words, model)
    return jsonify({'Books': result})

if __name__ == '__main__':
    app.run()
