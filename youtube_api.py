
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import isodate

import requests

# AIzaSyDPnnmHoDXUt0zm8z0JjgOaCNqmCd1BiqI



class YoutubeAPIService:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.api_service = self.get_api_service()
        self.base_url = base_url


    def get_api_service(self):
        return build('youtube', 'v3', developerKey=self.api_key)
    
    def get_channel_info(self, channel_id: str):
        """
        Fetch channel information for a given channel ID.

        Parameters:
            channel_id (str): The YouTube channel ID.

        Returns:
            dict: A dictionary containing channel information or None if the request fails.
        """
        params = {
            'key': self.api_key,
            'id': channel_id,
            'part': 'snippet,statistics'
        }
        response = requests.get("https://www.googleapis.com/youtube/v3/channels", params=params)
        if response.status_code == 200:
            response_json = response.json()
            if 'items' in response_json and len(response_json['items']) > 0:
                return response_json['items'][0]
        return None
    
    def search_videos(self, keywords, start_date, end_date, max_results=5):
        try:
            # Format the dates as strings
            start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

            # Call the YouTube API to search videos
            search_response = self.api_service.search().list(
                q=keywords,
                type='video',
                part='id,snippet',
                publishedAfter=start_date_str,
                publishedBefore=end_date_str,
                maxResults=max_results  # You can adjust this number based on your needs
            ).execute()
            videos = []
            for search_result in search_response.get('items', []):
                video_id = search_result['id']['videoId']
                video_info = self.get_video_info(video_id, update_task=False)
                videos.append(video_info)

            return videos

        except HttpError as e:
            print(f'An error occurred: {e}')




    def get_video_info(self, video_id, update_task):
        import pprint
        try:
            video_response = self.api_service.videos().list(
                part='snippet,statistics,contentDetails',
                id=video_id
            ).execute()

            if video_response['items']:
                video_info = video_response['items'][0]
                video_duration_iso_format = video_info['contentDetails']['duration']
                video_duration = isodate.parse_duration(video_duration_iso_format).total_seconds() / 3600
                video_duration = round(video_duration, 5)

                stats_info = {
                    'video_id': video_info['id'],
                    'views': video_info['statistics']['viewCount'],
                    'likeCount': video_info['statistics'].get('likeCount', 0),
                    'CommentCount': video_info['statistics'].get('commentCount', 0)
                    }
                if update_task:
                    return stats_info
                else:
                    channel_id = video_info['snippet']['channelId']
                    channel_info = self.get_channel_info(channel_id)
                    channel_subscribers = channel_info['statistics']['subscriberCount']
                    channel_country = channel_info['snippet'].get('country', 'world')
                    channel_description = channel_info['snippet'].get('description', None)
                    channel_name = channel_info['snippet']['title']
                    additional_info = {
                        'channel_subscribers': int(channel_subscribers),
                        'channel_tracker': channel_id,
                        'channel_name': channel_name, 
                        'channel_country': channel_country,
                        'channel_description': channel_description,
                        'duration': video_duration, 
                        'title': video_info['snippet']['title'], 
                        'publishedAt': video_info['snippet']['publishedAt']}
                    return {**stats_info, **additional_info}

        except HttpError as e:
            print(f'An error occurred: {e}')