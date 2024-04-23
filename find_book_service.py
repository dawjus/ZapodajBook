import pandas as pd


def find_book(title, df, matrix):
    #df = pd.read_csv('database/goodreads_data.csv')
    indexes = df.loc[df['Book'] == title].index
    if indexes.empty:
        return None
    else:
        books_index = match_book(indexes[0], matrix)
        books = []
        for ind in books_index:
            books.append(df.iloc[[ind]][['Book', 'Author']].to_dict(orient='records')[0])
        return books


def find_book_with_description(description, df, stop_words, model):
    user_description = preprocess(description, stop_words)
    descriptions = df['Description'].values
    result = []

    for i in range(3):
        database_description = preprocess(descriptions[i], stop_words)
        distance = calculate_distance_between_two_descriptions(model, user_description, database_description)
        result.append((i, distance))
    result = sorted(result, key=lambda x: x[0])

    n = 10 #len(descriptions)
    for i in range(3, n):
        database_description = preprocess(descriptions[i], stop_words)
        distance = calculate_distance_between_two_descriptions(model, user_description, database_description)
        if distance < result[-1][1]:
            result[-1] = (i, distance)
            result = sorted(result, key=lambda x: x[0], reverse=True)

    return match_description(result, df)


def match_book(index, matrix):
    sorted_indexes = sorted(range(len(matrix[index])), key=lambda i: matrix[index][i])
    return sorted_indexes[:3]

def match_description(indexes, df):
    result = []
    for ind, _ in indexes:
        result.append(df.iloc[[ind]][['Book', 'Author']].to_dict(orient='records')[0])
    return result

def preprocess(description, stop_words):
    return [w for w in description.lower().split() if w not in stop_words]

def calculate_distance_between_two_descriptions(model, desc1, desc2):
    return model.wmdistance(desc1, desc2)