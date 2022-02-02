import pandas as pd
import time

from data_processing import *
from model_utils import *

if __name__ == '__main__':
    start_time = time.time()
    print('Start calculating and saving embedding models and data...')
    ## File names
    # Input rating and book csv files
    ratings_file = 'data/BX-Book-Ratings.csv'
    books_file = 'data/BX-Books.csv'
    # column (index) to isbn array output file
    isbn_file = 'database_files/isbn.npy'
    # title output file
    title_file = 'database_files/title.pickle'
    # Truncated (top) rating data/matrix files
    num_high = 100
    high_ratings_file = 'database_files/high_ratings.npy'
    high_ratings_book_inds_file = 'database_files/high_ratings_book_inds.npy'
    # Output embedding files
    embed_mat_file = 'model_files/embed_mat.npy'
    db_file = 'database_files/embed_database.npy'

    ## Process data and calculate (sparse) rating matrix
    print('\nProcessing data and calculating rating matrix...')
    df_book = pd.read_csv(ratings_file, encoding='ISO-8859–1', sep=';', on_bad_lines='skip')
    df_title = pd.read_csv(books_file, encoding='ISO-8859–1', sep=';', on_bad_lines='skip')
    ratings = process_data(df_book, descr=['User-ID', 'ISBN', 'Book-Rating'], isbn_file=isbn_file)
    print('Done calculating rating matrix.')

    ## (Truncated) book and rating information
    print('\nCalculating title dictionary and truncated (top) rating data...')
    # Save ISBN to title dict/map
    process_title(df_title, title_file=title_file)
    # Calculate highest rating num_high books for each user
    high_ratings, high_ratings_book_inds = top_n_sparse(ratings, num_high)
    np.save(high_ratings_file, high_ratings)
    np.save(high_ratings_book_inds_file, high_ratings_book_inds)
    print('Done calculating title dictionary and truncated (top) rating data.')

    ## Calculate embedding information
    print('\nCalculating embedding information including embedding matrix and all users\' embedding vectors...')
    embed_dim = 100
    # Calculate and save embedding matrix
    embed_mat = calculate_embed_mat(ratings, embed_dim)
    np.save(embed_mat_file, embed_mat)
    # Calculate and save database's embedding matrix
    users_db = calculate_embed_vecs(ratings, embed_mat)
    np.save(db_file, users_db)
    print('Done calculating embedding information .')

    print('\nThe whole process takes {:.3f} seconds'.format(time.time()-start_time))