import re
from datetime import timedelta
from googleapiclient.discovery import build
from datetime import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
startTime = datetime.now()
api_key = 'AIzaSyCvUl9TOkkkB_p-NoE5sFYyUa1s7Cmpg5E'

youtube = build('youtube', 'v3', developerKey=api_key)


# video_url = request.GET.get('G0jO8kUrg-I')
 # api_key = 'AIzaSyCvUl9TOkkkB_p-NoE5sFYyUa1s7Cmpg5E'
# youtube = build('youtube', 'v3', developerKey=api_key)
# print(video_url)
video_id = "kJj8RR3SNTc"
request = youtube.commentThreads().list(
part="snippet",
videoId=video_id,
textFormat="plainText",
maxResults=100
)

# Execute the API request and retrieve the comments
comments = []
response = request.execute()
while response:
    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)
    if "nextPageToken" in response:
        request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        pageToken=response["nextPageToken"],
        maxResults=100
        )
        response = request.execute()
    else:
        break

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()
positive_comments = 0
negative_comments = 0
neutral_comments = 0
for comment in comments:
    sentiment = sia.polarity_scores(comment)
    if sentiment["compound"] > 0.05:
        positive_comments += 1
    elif sentiment["compound"] < -0.05:
        negative_comments += 1
    else:
        neutral_comments += 1

# Compute the percentage of positive, negative, and neutral comments
total_comments = len(comments)
positive = (positive_comments / total_comments) * 100
positive1 = round(positive, 2)
negative = (negative_comments / total_comments) * 100
negative1 = round(negative, 2)
neutral = (neutral_comments / total_comments) * 100
neutral1 = round(neutral, 2)
if type(positive1) == float:
    positive1 = str(positive1)
elif type(positive1) != list and type(positive1) != str:
    positive1 = ''+'\n'
if type(negative1) == float:
    negative1 = str(negative1)
elif type(negative1) != list and type(negative1) != str:
    negative1 = ''+'\n'
if type(neutral1) == float:
    neutral1 = str(neutral1)
elif type(neutral1) != list and type(neutral1) != str:
    neutral1 = ''
result = {
    'positive': positive1,
    'negative': negative1,
    'neutral': neutral1,
}
print(result)
