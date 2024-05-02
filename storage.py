from google.cloud import storage

def upload_to_bucket(project, credentials, bucket_name, blob_path, local_path):
    bucket = storage.Client(project=project, credentials=credentials).bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.upload_from_filename(local_path)
    return True