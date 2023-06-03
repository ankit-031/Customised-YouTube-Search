# from googleapiclient.discovery import build
# import pandas as pd
#
# from accounts.views import all_urls
#
#
# def get_related_videos(latest_video):
#     api_key = 'AIzaSyCvUl9TOkkkB_p-NoE5sFYyUa1s7Cmpg5E';#youtube's api key
#     youtube = build('youtube', 'v3', developerKey=api_key)
#     search_response = youtube.search().list(q=latest_video.keyword, part='id', type='video', maxResults=10).execute()
#     video_ids = [search_result['id']['videoId'] for search_result in search_response.get('items', [])]
#
#     # Get video details using videos API
#     video_response = youtube.videos().list(id=','.join(video_ids), part='snippet,statistics').execute()
#     videos = [{
#         'link': f'https://www.youtube.com/embed/{video["id"]}',
#         'title': video['snippet']['title'],
#         'views': int(video['statistics']['viewCount'])
#     } for video in video_response.get('items', [])]
#     return videos
#
#
# def getsearch_detials(youtube, keyword):
#     request = youtube.search().list(q=keyword, part='snippet,id', type='video', maxResults=50) #using youtube's inbuild function to get the list of vidoes of the searched keyword
#     response = request.execute()
#     return response # We get the response in json format
#
#
# def get_video_detials(youtube, video_ids):
#     all_video = []
#     request = youtube.videos().list(part='snippet,statistics', id=','.join(video_ids)) #Here we use the youtube's api inbuilt function to get the information about the number of views,comments and all other related information
#     response = request.execute()
#     for vid,video in zip(all_urls,response['items']):
#         video_data = dict(Url=vid,Video_title=video['snippet']['title'], Views=video['statistics']['viewCount'],LikeCount=int(video['statistics'].get('likeCount',0)),Comments=int(video['statistics'].get('commentCount',0)),Channel_id=video['snippet']['channelId'],Published_date=video['snippet']['publishedAt'])
#         all_video.append(video_data)
#     return all_video
#
