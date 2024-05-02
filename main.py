import os
import datetime

import pandas as pd
from fastapi import FastAPI
import uvicorn

from youtube_api import YoutubeAPIService
from auth import get_credentials
from storage import upload_to_bucket

app = FastAPI()

@app.get("/trigger-youtube-api-job")
async def retrieve_new_video_data():
    nb_days = 1
    max_search_results = 1
    api_key = "AIzaSyDPnnmHoDXUt0zm8z0JjgOaCNqmCd1BiqI"
    base_url = "https://www.googleapis.com/youtube/v3"
    project = 'My Fist Project'
    local_credentials_path = 'credentials.json'
    keysearch = "epita"


    # Create a new instance of the YoutubeAPIService class
    youtube_api_service = YoutubeAPIService(
        api_key=api_key, base_url=base_url)
    
    # get the youtube keysearch
    

    end_datetime = datetime.datetime.now(datetime.timezone.utc)
    start_datetime = end_datetime - datetime.timedelta(days=nb_days)

    videos = youtube_api_service.search_videos(
        keysearch, start_datetime, end_datetime, max_results=max_search_results)
    

    # create a new csv in cloud storage
    # upload the csv to the cloud storage
    # return the url of the csv

    local_file_path = f'{start_datetime.strftime("%Y-%m-%d")}_{end_datetime.strftime("%Y-%m-%d")}_{keysearch}_videos.csv'

    # write the videos to a CSV file
    df = pd.DataFrame(videos)
    df.to_csv(local_file_path, index=False)
    
    credentials = get_credentials(local_credentials_path)
    bucket_name = 'iaas_tp1_bucket_1' # do not give gs:// ,just bucket name
    blob_path = f'daily_search/{local_file_path}'
    upload_to_bucket(project, credentials, bucket_name, blob_path, local_file_path)

    # remove the local file
    os.remove(local_file_path)

    return {"message": "ok"}




if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
