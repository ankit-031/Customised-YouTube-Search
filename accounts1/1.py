


from googleapiclient.discovery import build
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# AIzaSyCvUl9TOkkkB_p-NoE5sFYyUa1s7Cmpg5E
api_key = 'AIzaSyCvUl9TOkkkB_p-NoE5sFYyUa1s7Cmpg5E'  # youtube's api key
# AIzaSyBd7nIaAUP0cpnC1AmSOf7wyjyNW9vOozE
youtube = build('youtube', 'v3', developerKey=api_key)
video_id='lJXta7ic9Rs'
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

nltk.download('vader_lexicon')
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
negative = (negative_comments / total_comments) * 100
neutral = (neutral_comments / total_comments) * 100
if type(positive) == float:
    positive = str(positive)
elif type(positive) != list and type(positive) != str:
    positive = ''
if type(negative) == float:
    negative = str(negative)
elif type(negative) != list and type(negative) != str:
    negative = ''
if type(neutral) == float:
    neutral = str(neutral)
elif type(neutral) != list and type(neutral) != str:
    neutral = ''
result = {
    'positive': positive,
    'negative': negative,
    'neutral': neutral,
}

print(result)