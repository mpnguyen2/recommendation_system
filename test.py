import os
import numpy as np
from data_transfer import *

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APP_CREDENTIALS

if __name__ == '__main__':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APP_CREDENTIALS
    bucket_name = 'recommendation_system_bucket2' 
    bucket = get_bucket(bucket_name)
    # Test upload file
    '''
    upload_file_to_bucket(bucket, gcp_file_name='data/test.txt', file_name='test.txt', content_type='text/txt')
    # Test up/load dict/pickle data
    dict_data = {'take': 4, 'go': 2, 'meow': 4, 'hello': 5}
    upload_data_to_bucket(bucket, file_name='data/test.pickle', data=dict_data, file_type='pickle')
    dict_data_get = get_file_from_bucket(bucket, 'data/test.pickle', 'pickle')
    print(dict_data_get)
    # Test load csv data
    df = get_file_from_bucket(bucket, 'data/BX-Book-Ratings.csv')
    print(df.head())
    '''
    # Test up/load numpy data
    numpy_data = np.random.rand(5, 2)
    print('Original data:')
    print(numpy_data)
    df = pd.DataFrame(numpy_data, )
    upload_data_to_bucket(bucket, file_name='data/test_npy.csv', data=df, file_type='csv')
    print('Done uploading numpy data as csv form.')
    numpy_data_get = get_file_from_bucket(bucket, 'data/test_npy.csv', sep=',').values[:, 1:]
    print('GCP data:')
    print(numpy_data_get)
    # Test getting all blobs
    print('\nAll blobs:')
    list_blobs(bucket_name)