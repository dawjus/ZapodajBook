from csv_parser import save_to_csv
import numpy as np
import pandas as pd
from gensim.models import KeyedVectors
from nltk import download
from nltk.corpus import stopwords


class BookDB:
    def __init__(self, df, model):
        self.df = df
        self.model = model
        self.matrix = self.create_matrix(df)

    def create_matrix(self, df):
        # size = df.shape[0]
        size = 6
        matrix = [[np.inf for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(i + 1, size):
                desc1 = self.preprocess(df.iloc[[i]]['Description'].values[0])
                desc2 = self.preprocess(df.iloc[[j]]['Description'].values[0])
                distance = self.calculate_distance_between_two_descriptions(desc1, desc2)
                matrix[i][j] = matrix[j][i] = distance
        return matrix

    def preprocess(self, description):
        return [w for w in description.lower().split() if w not in stop_words]

    def calculate_distance_between_two_descriptions(self, desc1, desc2):
        return self.model.wmdistance(desc1, desc2)




if __name__ == '__main__':
    model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300-SLIM.bin', binary=True)
    download('stopwords')
    stop_words = stopwords.words('english')
    df = pd.read_csv('../database/goodreads_data.csv')

    database = BookDB(df, model)
    save_to_csv(database.matrix, 'data.csv')
