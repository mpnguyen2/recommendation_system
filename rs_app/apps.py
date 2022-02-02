from django.apps import AppConfig
import numpy as np
from model_utils import *
import pickle

class RsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rs_app'
    # Embedding files
    db_file = 'database_files/embed_database.npy'
    embed_mat_file = 'model_files/embed_mat.npy'
    # Truncated (top) rating data/matrix
    high_ratings_file = 'database_files/high_ratings.npy'
    high_ratings_book_inds_file = 'database_files/high_ratings_book_inds.npy'
    # column (index) to isbn array 
    isbn_file = 'database_files/isbn.npy'
    # dictionary from isbn to title file
    title_file = 'database_files/title.pickle'

    if not (os.path.exists(db_file) or os.path.exist(embed_mat_file) or os.path.exist(high_ratings_file)):
        print('Model does not exist. Need to do computations before!!!')
        users_db = None
    else:
        # Load all user database's embedding matrix
        users_db = np.load(db_file)
        # Load embedding matrix
        embed_mat = np.load(embed_mat_file)
        # Load truncated (top) rating matrix and corresponding (book column) index matrix
        high_ratings = np.load(high_ratings_file)
        high_ratings_book_inds = np.load(high_ratings_book_inds_file)
        # Load column (index) to isbn array and dictionary from isbn to title file
        isbn = np.load(isbn_file)
        with open(title_file, 'rb') as handle:
            title = pickle.load(handle)
        # Number of book in database
        num_book = len(isbn)
        col_indices = None
