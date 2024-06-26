import os
import pandas as pd
from io import StringIO
from google.cloud import storage
from auth import get_credentials

def upload_to_bucket(project, credentials, bucket_name, blob_path, local_path):
    bucket = storage.Client(project=project, credentials=credentials).bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.upload_from_filename(local_path)
    return True

def download_and_process_blob(bucket, blob):
    """Downloads a blob and processes it directly into a DataFrame."""
    content = blob.download_as_text()
    df = pd.read_csv(StringIO(content))
    return df

def download_all_files_from_bucket(project, credentials, bucket_name):
    storage_client = storage.Client(project=project, credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()

    dataframes = []
    for blob in blobs:
        if blob.name.endswith('.csv'):
            df = download_and_process_blob(bucket, blob)
            dataframes.append(df)
            print(f"Blob {blob.name} processed into DataFrame.")
    
    return dataframes

if __name__ == '__main__':
    project = 'My First Project'
    local_credentials_path = 'credentials.json'
    credentials = get_credentials(local_credentials_path)
    bucket_name = 'iaas_tp1_bucket_1' # do not give gs:// ,just bucket name
    
    df = download_all_files_from_bucket(project, credentials, bucket_name)
    print(f"Downloaded {len(df)} CSV files.")
    for i, df in enumerate(df):
        df.to_csv(f'./downloaded_files/file_{i}.csv', index=False)
