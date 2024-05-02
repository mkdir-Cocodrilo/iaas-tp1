from google.oauth2 import service_account

def get_credentials(local_credentials_path):
    return service_account.Credentials.from_service_account_file(local_credentials_path)