import os
import time
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
from utils import read_all_csv_files
from auth import get_credentials
from storage import download_all_files_from_bucket

def insert_channel_data(df, engine):
    conn = engine.connect()
    new_channels = 0
    updated_channels = 0
    for _, row in df.iterrows():
        insert_query = text("""
            INSERT INTO channel (id, name, subscribers) 
            VALUES (:id, :name, :subscribers)
            ON CONFLICT (id) 
            DO UPDATE SET 
                name = EXCLUDED.name,
                subscribers = EXCLUDED.subscribers
        """)
        result = conn.execute(insert_query, {
            'id': row['channel_tracker'],
            'name': row['channel_name'],
            'subscribers': row['channel_subscribers']
        })
        if result.rowcount == 1:
            new_channels += 1
        else:
            updated_channels += 1
    conn.close()
    return new_channels, updated_channels

def insert_video_data(df, engine):
    conn = engine.connect()
    new_videos = 0
    updated_videos = 0
    for _, row in df.iterrows():
        insert_query = text("""
            INSERT INTO videos (id, title, date_created, channel_id, likes, comments, views)
            VALUES (:id, :title, :date_created, :channel_id, :likes, :comments, :views)
            ON CONFLICT (id)
            DO UPDATE SET
                title = EXCLUDED.title,
                date_created = EXCLUDED.date_created,
                channel_id = EXCLUDED.channel_id,
                likes = EXCLUDED.likes,
                comments = EXCLUDED.comments,
                views = EXCLUDED.views
        """)
        result = conn.execute(insert_query, {
            'id': row['video_id'],
            'title': row['title'],
            'date_created': row['publishedAt'],
            'channel_id': row['channel_tracker'],
            'likes': row['likeCount'],
            'comments': row['CommentCount'],
            'views': row['views']
        })
        if result.rowcount == 1:
            new_videos += 1
        else:
            updated_videos += 1
    conn.close()
    return new_videos, updated_videos

def insert_import_task_data(engine, start_time, end_time, status, nb_videos_created, nb_videos_updated):
    import_task = pd.DataFrame([{
        'start_import': start_time,
        'end_import': end_time,
        'status': status,
        'nb_videos_created': nb_videos_created,
        'nb_videos_updated': nb_videos_updated
    }])
    import_task.to_sql('importtask', engine, if_exists='append', index=False)
    print(f"Inserted import task data, {nb_videos_created} new videos, {nb_videos_updated} updated videos")

def process_dataframes(dataframes, engine):
    start_time = datetime.now()
    total_new_videos = 0
    total_updated_videos = 0
    status = 'Completed'

    try:
        for df in dataframes:
            _, _ = insert_channel_data(df, engine)  # Channels are not counted in import task
            new_videos, updated_videos = insert_video_data(df, engine)
            total_new_videos += new_videos
            total_updated_videos += updated_videos
    except Exception as e:
        print(f"Error processing dataframes: {e}")
        status = 'Error'

    end_time = datetime.now()
    status = 'Completed'
    insert_import_task_data(engine, start_time, end_time, status, total_new_videos, total_updated_videos)
    print("Processed dataframes")

if __name__ == "__main__":
    try :
        print("Starting script...")
        project = 'My First Project'
        local_credentials_path = 'credentials.json'
        print(f"Reading credentials from {local_credentials_path}")
        credentials = get_credentials(local_credentials_path)
        print("Credentials read successfully!")
        bucket_name = 'iaas_tp1_bucket_1' # do not give gs:// ,just bucket name
        
        print(f"Downloading files from bucket {bucket_name}")
        dataframes = download_all_files_from_bucket(project, credentials, bucket_name)
        print(f"Downloaded {len(dataframes)} CSV files.")

        print("Waiting for the database to be ready...")
        time.sleep(10)  # Wait for the database to be ready

        print("Connecting to the database...")
        connection_string = os.getenv('DATABASE_URL')
        print(f"Connection string: {connection_string}")
        engine = create_engine(connection_string)
        print("Connection established!")
        
        print("Processing dataframes...")
        process_dataframes(dataframes, engine)
        print("Dataframes processed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        start_time = datetime.now()
        end_time = datetime.now()
        insert_import_task_data(engine, start_time, end_time, 'Error', 0, 0)

