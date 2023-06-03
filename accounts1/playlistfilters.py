# import re
# from datetime import timedelta
# from googleapiclient.discovery import build
# from datetime import datetime
# import math

# startTime = datetime.now()
# playlist_dict = {}
# # Set up the YouTube API client
# # api_key = 'AIzaSyCvUl9TOkkkB_p-NoE5sFYyUa1s7Cmpg5E'
# # api_key='AIzaSyA9LH4mrYHWO4Dgwpl2uTuPGwgUlszaB7E'
# api_key='AIzaSyCA1vWMELDzSqGgJFrZ6ydXZBghnx0PcHY'
# # api_key='AIzaSyA3PgXGRyUXAkp8Um4jR-QMTXh-JdiS5JI'
# youtube = build('youtube', 'v3', developerKey=api_key)

# # Set up search parameters
# def getplaylist(keyword):
#     search_query = keyword
#     max_results = 10
#     type_filter = "playlist"

#     # Search for playlists based on the search query and type filter
#     playlist_data = []
#     request = youtube.search().list(
#         q=search_query,
#         type=type_filter,
#         part="id,snippet",
#         maxResults=max_results
#     )
#     response = request.execute()
#     playlist_ids = []
#     for item in response["items"]:
#         if item["id"]["kind"] == "youtube#playlist":
#             playlist_id = item["id"]["playlistId"]
#             playlist_title = item["snippet"]["title"]
#             playlist_url = f"https://www.youtube.com/playlist?list={item['id']['playlistId']}"
#             playlist_data.append((playlist_id, playlist_title, playlist_url))
#             # add the playlist_title to the playlist_dict dictionary
#             playlist_dict[playlist_id] = {'title': playlist_title}

#     # Calculate the total number of views, duration and standard deviation for each playlist and store in a dictionary

#     for playlist_id, playlist_title, playlist_url in playlist_data:
#         videos = []
#         nextPageToken = ''
#         while nextPageToken is not None:
#             request = youtube.playlistItems().list(
#                 part="contentDetails",
#                 playlistId=playlist_id,
#                 maxResults=50,
#                 pageToken=nextPageToken
#             )
#             response = request.execute()
#             videos.extend(response['items'])
#             nextPageToken = response.get('nextPageToken')

#         total_duration = timedelta()
#         view_count = 0
#         durations = []
#         video_count = len(videos) # Get the number of videos in the playlist
#         for video in videos:
#             video_id = video['contentDetails']['videoId']
#             request = youtube.videos().list(
#                 part="contentDetails,statistics",
#                 id=video_id
#             )
#             response = request.execute()
#             items = response.get('items', []) # Check if 'items' exists in the response
#             if not items: # Skip if 'items' is empty
#                 continue
#             duration = items[0]['contentDetails']['duration']
#             duration_components = re.findall(r'\d+', duration)
#             hours = int(duration_components[-3]) if len(duration_components) == 4 else 0
#             minutes = int(duration_components[-2])
#             seconds = int(duration_components[-1])
#             total_duration += timedelta(hours=hours, minutes=minutes, seconds=seconds)

#             view_count += int(items[0]['statistics']['viewCount'])
#             durations.append(int(re.findall('\d+', duration)[-1]))

#         # Calculate standard deviation
#         mean = sum(durations) / len(durations)
#         variance = sum((x - mean) ** 2 for x in durations) / len(durations)
#         std_deviation = math.sqrt(variance)

#         # Add playlist to dictionary
#         playlist_dict[playlist_id] = {
#             'url': playlist_url,
#             'playlist_id':playlist_url.split('=')[1],
#             'title': playlist_title,
#             'duration': int(total_duration.total_seconds()),
#             'view_count': view_count,
#             'std_deviation': std_deviation,
#             'total_time': str(total_duration),
#             'video_count': video_count,
#             'hours':int(int(total_duration.total_seconds())/60),
#             'minutes':int(int(total_duration.total_seconds())%60)
#         }

#     return playlist_dict
# v=getplaylist("java")

# print(v)




import re
from datetime import timedelta
from googleapiclient.discovery import build
from datetime import datetime
import math

startTime = datetime.now()
playlist_dict = {}
# Set up the YouTube API client
# api_key = 'AIzaSyCvUl9TOkkkB_p-NoE5sFYyUa1s7Cmpg5E'
# api_key='AIzaSyA9LH4mrYHWO4Dgwpl2uTuPGwgUlszaB7E'
api_key='AIzaSyCA1vWMELDzSqGgJFrZ6ydXZBghnx0PcHY'
# api_key='AIzaSyA3PgXGRyUXAkp8Um4jR-QMTXh-JdiS5JI'
youtube = build('youtube', 'v3', developerKey=api_key)

# Set up search parameters
def getplaylist(keyword):
    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')

    
    search_query = keyword
    max_results = 10
    type_filter = "playlist"

    # Search for playlists based on the search query and type filter
    playlist_data = []
    request = youtube.search().list(
        q=search_query,
        type=type_filter,
        part="id,snippet",
        maxResults=max_results
    )
    response = request.execute()
    playlist_ids = []
    for item in response["items"]:
        if item["id"]["kind"] == "youtube#playlist":
            playlist_id = item["id"]["playlistId"]
            playlist_title = item["snippet"]["title"]
            playlist_url = f"https://www.youtube.com/playlist?list={item['id']['playlistId']}"
            playlist_data.append((playlist_id, playlist_title, playlist_url))
            # add the playlist_title to the playlist_dict dictionary
            playlist_dict[playlist_id] = {'title': playlist_title}

    # Calculate the total number of views, duration and standard deviation for each playlist and store in a dictionary

    for playlist_id, playlist_title, playlist_url in playlist_data:
        videos = []
        nextPageToken = ''
        while nextPageToken is not None:
            request = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=nextPageToken
            )
            response = request.execute()
            videos.extend(response['items'])
            nextPageToken = response.get('nextPageToken')

        total_duration = timedelta()
        view_count = 0
        total_sec = 0   
        durations = []
        video_count = len(videos) # Get the number of videos in the playlist
        for video in videos:
            video_id = video['contentDetails']['videoId']
            request = youtube.videos().list(
                part="contentDetails,statistics",
                id=video_id
            )
            response = request.execute()
            items = response.get('items', []) # Check if 'items' exists in the response
            if not items: # Skip if 'items' is empty
                continue
            duration = items[0]['contentDetails']['duration']
            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = seconds_pattern.search(duration)

            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0

            video_seconds = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            ).total_seconds()

            total_sec += video_seconds
            view_count += int(items[0]['statistics']['viewCount'])
            durations.append(int(re.findall('\d+', duration)[-1]))

        # Calculate standard deviation
        mean = sum(durations) / len(durations)
        variance = sum((x - mean) ** 2 for x in durations) / len(durations)
        std_deviation = math.sqrt(variance)
        half_count = len(durations) // 2
        half_durations = durations[:half_count]
        mean = sum(half_durations) / len(half_durations)
        variance = sum((x - mean) ** 2 for x in half_durations) / len(half_durations)
        std_deviation2 = math.sqrt(variance)
        minutes, seconds = divmod(total_sec, 60)
        hours, minutes = divmod(minutes, 60)
        # Add playlist to dictionary
        playlist_dict[playlist_id] = {
            'standard-half':std_deviation2,
            'url': playlist_url,
            'playlist_id':playlist_url.split('=')[1],
            'title': playlist_title,
            'duration': total_sec,
            'view_count': view_count,
            'std_deviation': std_deviation,
            'total_time': str(total_sec),
            'video_count': video_count,
            'hours':int(hours),
            'minutes':int(minutes)
        }

    return playlist_dict


v=getplaylist("html")
print(v)
