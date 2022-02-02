from data_processing import *
from model_utils import *

'''
A = create_sparse_mat_from_dict(4000, 100000, {0:{1:2, 2:4}, 1:{2:10}})
top_n_value, top_n_idx = top_n_sparse(A, 5)
print(top_n_value[:2])
print(top_n_idx[:2])
'''

isbn = np.load('database_files/isbn.npy')

title_file = 'database_files/title.pickle'
with open(title_file, 'rb') as handle:
    title = pickle.load(handle)

col_indices = np.random.randint(low=0, high=len(isbn), size=10)
titles, _ = return_random_titles(col_indices, isbn, title)
print(titles)