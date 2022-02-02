import numpy as np
import scipy.sparse as sp
import pandas as pd
import pickle
from tqdm import tqdm

# Create sparse matrix from dictionary
def create_sparse_mat_from_dict(row, col, mat_dict):
    mat = sp.dok_matrix((row, col), dtype=float)
    for i in mat_dict.keys():
        for j in mat_dict[i].keys():
            mat[i, j] = mat_dict[i][j]
    return mat.tocsr()

def process_row_data(user_id, isbn, book_rating, user_to_row, row_to_user, book_to_column, column_to_book, mat):
    if user_id not in user_to_row:
        user_to_row[user_id] = len(row_to_user)
        mat[len(row_to_user)] = {}
        row_to_user.append(user_id)

    if isbn not in book_to_column:
        book_to_column[isbn] = len(column_to_book)
        column_to_book.append(isbn)

    mat[user_to_row[user_id]][book_to_column[isbn]] = book_rating

# Return a weighted tf-idf rating matrix, a map from user-ID to row index and from ISBN (book-ID) to column index
def process_data(df, descr, isbn_file, log_interval=10000):
    user_id, isbn, book_rating = descr
    user_to_row, book_to_column = {}, {}
    row_to_user, column_to_book = [], []
    mat_dict = {}

    pbar = tqdm(df.iterrows())
    for index, row in pbar:
        process_row_data(row[user_id], row[isbn], row[book_rating], user_to_row, row_to_user, book_to_column, column_to_book, mat_dict)
        if (index+1)%log_interval == 0:
            pbar.set_description("Processed %d rows" % index)
    print('Done processing data. Creating sparse matrix...')

    # Convert rating double-dictionary to scipy sparse matrix
    mat = create_sparse_mat_from_dict(len(row_to_user), len(column_to_book), mat_dict)

    # Save column to isbn array
    np.save(isbn_file, np.array(column_to_book))

    print('Done processing data.')

    return mat

# Create a map from ISBN to the corresponding title's book
def process_title(df_title, isbn_colname='ISBN', title_colname='Book-Title', title_file='title.pickle'):
    isbn_to_title = {}
    titles = df_title[title_colname].values
    isbns = df_title[isbn_colname].values
    for i in range(len(titles)):
        isbn_to_title[isbns[i]] = titles[i]

    with open(title_file, 'wb') as handle:
            pickle.dump(isbn_to_title, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('Done and save titles.')