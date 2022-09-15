import io
import pandas as pd
import pickle
from google.cloud import storage
from secret_fields import GOOGLE_APP_CREDENTIALS

def get_bucket(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    return bucket

def get_file_from_bucket(bucket, file_name, file_type='csv', meta_data=[], sep=';'):
    blob = bucket.blob(file_name)
    if file_type == 'txt':
        return blob.download_as_string()
    elif file_type == 'csv':
        data = blob.download_as_string()
        if len(meta_data) != 0:
            return pd.read_csv(io.BytesIO(data), encoding='ISO-8859–1', sep=sep, on_bad_lines='skip', dtype=meta_data[0])
        else:
            return pd.read_csv(io.BytesIO(data), encoding='ISO-8859–1', sep=sep, on_bad_lines='skip')
    elif file_type == 'pickle':
        data = blob.download_as_string()
        return pickle.loads(data)

def upload_data_to_bucket(bucket, file_name, data, file_type='csv'):
    blob = bucket.blob(file_name)
    if file_type == 'csv':
        blob.upload_from_string(data.to_csv(), 'text/csv')
    elif file_type == 'pickle':
        pickle_data = pickle.dumps(data)
        blob.upload_from_string(pickle_data)

def upload_file_to_bucket(bucket, gcp_file_name, file_name, content_type):
    blob = bucket.blob(gcp_file_name)
    blob.upload_from_filename(file_name, content_type=content_type)

def list_blobs(bucket_name):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)
    for blob in blobs:
        print(blob.name)