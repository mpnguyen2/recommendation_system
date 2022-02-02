import scipy.sparse as sp
import scipy.sparse.linalg as sp_linalg
import numpy as np
import os
import heapq

# Calculate embedding matrix (for row vector) given user-book matrix A
def calculate_embed_mat(A, embed_dim):
    _, S, Vt = sp_linalg.svds(A, k=embed_dim)
    
    return np.dot(np.diag(1.0/S), Vt)

# Calculate embedding vector for user ratings packed in a matrix user_data given embedded matrix embed_mat
def calculate_embed_vecs(ratings, embed_mat):
    # ratings dim = (#users, #books)
    # embed_mat dim = (embed_dim, #books)
    # Need to return matrix of dim = (embed_dim, #users)
    return ratings.dot(embed_mat.transpose()).transpose()

# Embed and then compare user_rating with embedded vector in the database 
def find_top_similar_users(user_ratings, embed_mat, high_ratings, high_ratings_book_inds,
    users_db, isbn, title, num_similar_users=10, num_book_returns=20):

    # Calculate user embedding vector
    user_vec = calculate_embed_vecs(user_ratings.reshape(1, -1), embed_mat)
    user_vec /= np.linalg.norm(user_vec)
    # Find top users that are similar to the query user
    similarity = np.dot(user_vec.reshape(1, -1), users_db).reshape(-1)
    top_users = np.argsort(similarity)[:num_similar_users]
    # Find top books rated highest by those top users and return their title
    ratings = high_ratings[top_users]
    book_inds = high_ratings_book_inds[top_users]
    h = []
    set_check = set()
    for i in range(ratings.shape[0]):
        for j in range(ratings.shape[1]):
            book_ind = book_inds[i][j]
            if book_ind in set_check:
                continue
            if len(h) < num_book_returns:
                heapq.heappush(h, (ratings[i][j], book_ind))
            else:
                heapq.heappushpop(h, (ratings[i][j], book_ind))
            set_check.add(book_ind)

    titles_result = []
    for e in h:
        isbn_str = str(isbn[int(e[1])])
        if isbn_str in title:
            titles_result.append(title[isbn_str])
    return titles_result

## Calculate top n values/indices for each row in a sparse matrix
def fill_in_values(data, n):
    if len(data) == n:
        return data
    return np.concatenate((data, np.zeros(n-data.shape[0])))

def fill_in_indices(indices, n):
    indices_set = set(indices)
    fill_indices = list(indices)
    ind = 0
    while len(fill_indices) < n:
        while ind in indices_set:
            ind += 1
        fill_indices.append(ind)
        ind += 1
    
    return np.array(fill_indices)

def top_n_sparse(mat, n):
    num_row = mat.shape[0]
    top_n_idx = np.zeros((num_row, n))
    top_n_value = np.zeros((num_row, n))
    for i in range(num_row):
        l_row, r_row = mat.indptr[i], mat.indptr[i+1]
        n_row_pick = min(n, r_row - l_row)
        inds = l_row + np.argpartition(mat.data[l_row:r_row], -n_row_pick)[-n_row_pick:]
        
        top_n_idx[i] = fill_in_indices(mat.indices[inds], n)
        top_n_value[i] = fill_in_values(mat.data[inds], n)
        
    return top_n_value, top_n_idx

# Helper function for view: Return random titles and then take user ratings vector from partial rating
def return_random_titles(col_indices, isbn, title):
    random_titles = []
    # It can happen that isbn[col_indices] may have no corresponding title 
    valid_col_indices = []
    for ind in col_indices:
        isbn_str = str(isbn[ind])
        if isbn_str in title:
            random_titles.append(title[isbn_str])
            valid_col_indices.append(ind)
    return random_titles, np.array(valid_col_indices)

def find_user_ratings(col_indices, partial_ratings, num_book):
    user_ratings = np.zeros(num_book)
    user_ratings[col_indices] = partial_ratings
    return user_ratings