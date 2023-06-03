import re
from googleapiclient.discovery import build
from datetime import timedelta

# Set up the YouTube API client
api_key = 'YOUR_API_KEY_HERE'
youtube = build('youtube', 'v3', developerKey=api_key)

# Set up search parameters
search_query = "python tutorial"
max_results = 50
type_filter = "video"

# Search for videos based on the search query and type filter
video_ids = []
request = youtube.search().list(
    q=search_query,
    type=type_filter,
    part="id",
    maxResults=max_results
)
response = request.execute()
for item in response["items"]:
    if item["id"]["kind"] == "youtube#video":
        video_ids.append(item["id"]["videoId"])

# Retrieve the duration of each video and print the URLs of videos with duration less than 30 minutes
for video_id in video_ids:
    request = youtube.videos().list(
        part="contentDetails",
        id=video_id
    )
    response = request.execute()
    duration = response['items'][0]['contentDetails']['duration']
    total_duration = timedelta(seconds=int(re.findall('\d+', duration)[-1]))
    if total_duration < timedelta(minutes=30):
        print(f"https://www.youtube.com/watch?v={video_id}")