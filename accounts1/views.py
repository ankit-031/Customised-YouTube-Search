import email
import json

from django.template.loader import render_to_string
from django.utils.datetime_safe import date
from .playlistfilters import getplaylist
from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.http import JsonResponse
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from .helpers import send_forget_password_mail
import uuid
from send_mail_app.tasks import send_mail_func, send_mail_forget
# send_mail_app.tasks if change

# from django.core.mail import send_mail
import uuid
from django.conf import settings
from .tasks import *
from .models import SearchModel
# from .youtube import *
from googleapiclient.discovery import build
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# AIzaSyCvUl9TOkkkB_p-NoE5sFYyUa1s7Cmpg5E
api_key = 'AIzaSyCvUl9TOkkkB_p-NoE5sFYyUa1s7Cmpg5E'  # youtube's api key
# AIzaSyBd7nIaAUP0cpnC1AmSOf7wyjyNW9vOozE
youtube = build('youtube', 'v3', developerKey=api_key)


# api_key = 'AIzaSyBd7nIaAUP0cpnC1AmSOf7wyjyNW9vOozE';  # youtube's api key
# youtube = build('youtube', 'v3', developerKey=api_key)  # build using youtube's api method

# \ Filters

# 10 30 1hr 3hr above 5

# Create your views here.
def index(request):
    return render(request, "1.html")


def CustomSearch(request):
    return render(request, "CustomSearch.html")


def about_us(request):
    return render(request, "aboutus.html")


def showVideo(request):
    try:
        if request.method == 'POST':
            keyword = request.POST.get('keyword')
            category = request.POST.get('length')
            print(category)
            if not keyword:
                return render(request, "CustomSearch.html")

            print(keyword)
            post = SearchModel()
            post.keyword = keyword
            post.category = category
            user = request.user
            user_id = user.id
            post.user_id = user_id
            post.save();

            if category == 'video':
                latest_video = SearchModel.objects.latest('id')
                videos = get_related_videos(latest_video)
                context = {'videos': videos, 'keyword': latest_video.keyword}
                return render(request, 'show.html', context)
                # return redirect('/ShowVideo')
            elif category == 'playlist':
                context=getplaylist(keyword)
                playlist_query = Playlist.objects.filter(keyword=keyword)
                
                for playlist_id, playlist_data in context.items():
                    playlist = Playlist(keyword=keyword, title=playlist_data["title"], view_count=playlist_data["view_count"],pid=playlist_id,se=playlist_data["std_deviation"],vc=playlist_data["video_count"],time=playlist_data["duration"],hours=playlist_data["hours"],minutes=playlist_data["minutes"])
                    playlist.save()
                return render(request, 'playlist_result.html',{'playlists': context,'keyword': keyword})
            # elif category == 'playlist':
            #     playlist_query = Playlist.objects.filter(keyword=keyword)
            #     context = {}
            #     for playlist in playlist_query:
            #         context[playlist.pid] = {
            #             'title': playlist.title,
            #             'view_count': playlist.view_count,
            #             'std_deviation': playlist.se,
            #             'video_count': playlist.vc,
            #             'duration': playlist.time,
            #             'hours':playlist.hours,
            #             'minutes':playlist.minutes,
            #     }
            #     return render(request, 'playlist_result.html', {'playlists': context, 'keyword': keyword})
            elif category == 'channel':
                return redirect('/ShowChannel')
        else:
            return render(request, "show.html")
    except Exception as e:
        print(e)
        return render(request, "CustomSearch.html")


# def duration_to_seconds(duration):
#     if 'P' in duration:
#         days, time = duration.split('T')
#         days = days.replace('P', '')
#     else:
#         time = duration
#
#     if ':' in time:
#         hours, minutes, seconds = map(int, time.split(':'))
#         total_seconds = hours * 3600 + minutes * 60 + seconds
#     else:
#         total_seconds = int(time)
#
#     if 'days' in locals():
#         total_seconds += int(days) * 24 * 3600
#
#     return total_seconds


def update_result(request):
    # data = json.loads(request.body)
    # declarations
    video_ids = []
    all_urls = []
    date1 = []
    month = []
    year = []
    dat = []
    customdetails = []
    all = []
    days1 = []
    months1 = []
    years1 = []
    views = []
    comments = []
    urlss = []
    titles = []
    tot_days = []
    likes = []
    perdayl = []
    channel = []
    csub = [0] * 50
    # option = "month"
    ctitle = []
    mfinal = []
    mperdayl = []
    mperdaysc = []
    mperdaysv = []
    yperdayl = []
    yperdaysv = []
    yperdaysc = []
    final = []
    perdaysv = []
    perdaysc = []

    option1 = request.POST.get("one")
    option2 = request.POST.get("two")
    option3 = request.POST.get("three")
    option4 = request.POST.get("select-option")
    print(option1)
    print(option2)
    print(option3)
    print(option4)
    sliderValue = request.POST.get("slider")
    sliderValue1 = request.POST.get("slider1")
    sliderValue2 = request.POST.get("slider2")
    sliderrValue = request.POST.get("sliderr");
    sliderrValue1 = request.POST.get("sliderr1");
    sliderrValue2 = request.POST.get("sliderr2");

    if sliderValue is not None:
        sliderValuee = float(sliderValue)
    else:
        sliderValuee = 0.0

    if sliderValue1 is not None:
        sliderValuee1 = float(sliderValue1)
    else:
        sliderValuee1 = 0.0

    if sliderValue2 is not None:
        sliderValuee2 = float(sliderValue2)
    else:
        sliderValuee2 = 0.0

    if sliderrValue is not None:
        sliderrValuee = float(sliderrValue)
    else:
        sliderrValuee = 0.0

    if sliderrValue1 is not None:
        sliderrValuee1 = float(sliderrValue1)
    else:
        sliderrValuee1 = 0.0

    if sliderrValue2 is not None:
        sliderrValuee2 = float(sliderrValue2)
    else:
        sliderrValuee2 = 0.0

        # sliderValuee1 = float(sliderValue1)
    # sliderValuee2 = float(sliderValue2)
    # sliderrValuee = float(sliderrValue)
    # sliderrValuee1 = float(sliderrValue1)
    # sliderrValuee2 = float(sliderrValue2)
    print(sliderValue)
    print(sliderValue1)
    print(sliderValue2)
    print(sliderrValue)
    print(sliderrValue1)
    print(sliderrValue2)

    latest_video = SearchModel.objects.latest('id')
    keyword = latest_video.keyword
    print(keyword)
    if option2 == 'rating' and option3=='ten':
        print("hello rating")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials1(youtube, video_ids, all_urls,600)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        print(sliderrValue)
        print(sliderrValue1)
        print(sliderrValue2)

        if sliderrValuee + sliderrValuee1 + sliderrValuee2 == 1:
            for i in range(len(video_data)):
                tot = int(
                    (views[0][i] * sliderrValuee) + (comments[0][i] * sliderrValuee1) + (likes[0][i] * sliderrValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }
            video.append(video_dict)

        # print(video)
        context = {'videos': video, 'keyword': keyword}

        return render(request, 'show.html', context)
    elif option2 == 'rating' and option3=='one hr':
        print("hello rating")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials1(youtube, video_ids, all_urls,3600)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        print(sliderrValue)
        print(sliderrValue1)
        print(sliderrValue2)

        if sliderrValuee + sliderrValuee1 + sliderrValuee2 == 1:
            for i in range(len(video_data)):
                tot = int(
                    (views[0][i] * sliderrValuee) + (comments[0][i] * sliderrValuee1) + (likes[0][i] * sliderrValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }
            video.append(video_dict)

        # print(video)
        context = {'videos': video, 'keyword': keyword}

        return render(request, 'show.html', context)
    elif option2 == 'rating' and option3=='1to3hr':
        print("hello rating")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials2(youtube, video_ids, all_urls)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        print(sliderrValue)
        print(sliderrValue1)
        print(sliderrValue2)

        if sliderrValuee + sliderrValuee1 + sliderrValuee2 == 1:
            for i in range(len(video_data)):
                tot = int(
                    (views[0][i] * sliderrValuee) + (comments[0][i] * sliderrValuee1) + (likes[0][i] * sliderrValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }
            video.append(video_dict)

        # print(video)
        context = {'videos': video, 'keyword': keyword}

        return render(request, 'show.html', context)
    elif option2 == 'rating' and option3=='above3':
        print("hello rating")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials3(youtube, video_ids, all_urls)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        print(sliderrValue)
        print(sliderrValue1)
        print(sliderrValue2)

        if sliderrValuee + sliderrValuee1 + sliderrValuee2 == 1:
            for i in range(len(video_data)):
                tot = int(
                    (views[0][i] * sliderrValuee) + (comments[0][i] * sliderrValuee1) + (likes[0][i] * sliderrValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }
            video.append(video_dict)

        # print(video)
        context = {'videos': video, 'keyword': keyword}

        return render(request, 'show.html', context)
    elif option2 == 'upload' and option4 == 'per-day' and option3=='ten':
        print("hello PER-DAY")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials1(youtube, video_ids, all_urls,600)
        print("hello")
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])
        print("hello")
        for i in range(len(video_data)):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)
        for i in range(len(video_data)):
            day = (today) - (dat[i])
            day = day.days
            days1.append(day)
        for i in range(len(video_data)):
            if days1[i] == 0:
                days1[i] = 1
            perdayviews = views[0][i] / days1[i]
            perdaycom = comments[0][i] / days1[i]
            perdaylike = likes[0][i] / days1[i]
            perdayl.append(perdaylike)
            perdaysv.append(perdayviews)
            perdaysc.append(perdaycom)

        if sliderValuee + sliderValuee1 + sliderValuee2 == 1:
            print("upload per-day")
            for i in range(len(video_data)):
                tot = int((perdaysv[i] * sliderValuee) + (perdaysc[i] * sliderValuee1) + (perdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)
        context = {'videos': video, 'keyword': keyword}
        print("hello")

        return render(request, 'show.html', context)
    elif option2 == 'upload' and option4 == 'per-day' and option3=='one hr':
        print("hello PER-DAY")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials1(youtube, video_ids, all_urls,3600)
        print("hello")
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])
        print("hello")
        for i in range(len(video_data)):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)
        for i in range(len(video_data)):
            day = (today) - (dat[i])
            day = day.days
            days1.append(day)
        for i in range(len(video_data)):
            if days1[i] == 0:
                days1[i] = 1
            perdayviews = views[0][i] / days1[i]
            perdaycom = comments[0][i] / days1[i]
            perdaylike = likes[0][i] / days1[i]
            perdayl.append(perdaylike)
            perdaysv.append(perdayviews)
            perdaysc.append(perdaycom)

        if sliderValuee + sliderValuee1 + sliderValuee2 == 1:
            print("upload per-day")
            for i in range(len(video_data)):
                tot = int((perdaysv[i] * sliderValuee) + (perdaysc[i] * sliderValuee1) + (perdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)
        context = {'videos': video, 'keyword': keyword}
        print("hello")

        return render(request, 'show.html', context)
    elif option2 == 'upload' and option4 == 'per-day' and option3=='1to3hr':
        print("hello PER-DAY")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials2(youtube, video_ids, all_urls)
        print("hello")
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])
        print("hello")
        for i in range(len(video_data)):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)
        for i in range(len(video_data)):
            day = (today) - (dat[i])
            day = day.days
            days1.append(day)
        for i in range(len(video_data)):
            if days1[i] == 0:
                days1[i] = 1
            perdayviews = views[0][i] / days1[i]
            perdaycom = comments[0][i] / days1[i]
            perdaylike = likes[0][i] / days1[i]
            perdayl.append(perdaylike)
            perdaysv.append(perdayviews)
            perdaysc.append(perdaycom)

        if sliderValuee + sliderValuee1 + sliderValuee2 == 1:
            print("upload per-day")
            for i in range(len(video_data)):
                tot = int((perdaysv[i] * sliderValuee) + (perdaysc[i] * sliderValuee1) + (perdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)
        context = {'videos': video, 'keyword': keyword}
        print("hello")

        return render(request, 'show.html', context)
    elif option2 == 'upload' and option4 == 'per-day' and option3=='above3':
        print("hello PER-DAY")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials3(youtube, video_ids, all_urls)
        print("hello")
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])
        print("hello")
        for i in range(len(video_data)):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)
        for i in range(len(video_data)):
            day = (today) - (dat[i])
            day = day.days
            days1.append(day)
        for i in range(len(video_data)):
            if days1[i] == 0:
                days1[i] = 1
            perdayviews = views[0][i] / days1[i]
            perdaycom = comments[0][i] / days1[i]
            perdaylike = likes[0][i] / days1[i]
            perdayl.append(perdaylike)
            perdaysv.append(perdayviews)
            perdaysc.append(perdaycom)

        if sliderValuee + sliderValuee1 + sliderValuee2 == 1:
            print("upload per-day")
            for i in range(len(video_data)):
                tot = int((perdaysv[i] * sliderValuee) + (perdaysc[i] * sliderValuee1) + (perdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)
        context = {'videos': video, 'keyword': keyword}
        print("hello")

        return render(request, 'show.html', context)
    if option2 == 'upload' and option4 == 'per-month' and option3=='ten':
        print("hello per-month")
        res = getsearch_detials(youtube, keyword)

        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)

        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials1(youtube, video_ids, all_urls,600)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released

        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])

        for i in range(len(video_data)):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)

        for i in range(len(video_data)):
            delta = today - dat[i]
            Months = delta.days / 30.44
            months1.append(Months)
        for i in range(len(video_data)):
            if months1[i] == 0:
                months1[i] = 1
            li = months1[i], views[0][i], comments[0][i]
            mperdayviews = views[0][i] / months1[i]
            mperdaycom = comments[0][i] / months1[i]
            mperdaylike = likes[0][i] / months1[i]
            final.append(li)
            mperdayl.append(mperdaylike)
            mperdaysv.append(mperdayviews)
            mperdaysc.append(mperdaycom)

        print(sliderValuee)
        print(sliderValuee1)
        print(sliderValuee2)

        tot1 = sliderValuee + sliderValuee1 + sliderValuee2
        print(tot1)
        if tot1 == 1:
            print("if")
            for i in range(len(video_data)):
                tot = int(
                    (mperdaysv[i] * sliderValuee) + (mperdaysc[i] * sliderValuee1) + (mperdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        # top10
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)
        context = {'videos': video, 'keyword': keyword}
        print("hello")
        # context = {'videos': top10, 'keyword': keyword}
        return render(request, 'show.html', context)
    if option2 == 'upload' and option4 == 'per-month' and option3=='one hr':
        print("hello per-month")
        res = getsearch_detials(youtube, keyword)

        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)

        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials1(youtube, video_ids, all_urls,3600)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released

        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])

        for i in range(len(video_data)):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)

        for i in range(len(video_data)):
            delta = today - dat[i]
            Months = delta.days / 30.44
            months1.append(Months)
        for i in range(len(video_data)):
            if months1[i] == 0:
                months1[i] = 1
            li = months1[i], views[0][i], comments[0][i]
            mperdayviews = views[0][i] / months1[i]
            mperdaycom = comments[0][i] / months1[i]
            mperdaylike = likes[0][i] / months1[i]
            final.append(li)
            mperdayl.append(mperdaylike)
            mperdaysv.append(mperdayviews)
            mperdaysc.append(mperdaycom)

        print(sliderValuee)
        print(sliderValuee1)
        print(sliderValuee2)

        tot1 = sliderValuee + sliderValuee1 + sliderValuee2
        print(tot1)
        if tot1 == 1:
            print("if")
            for i in range(len(video_data)):
                tot = int(
                    (mperdaysv[i] * sliderValuee) + (mperdaysc[i] * sliderValuee1) + (mperdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        # top10
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)
        context = {'videos': video, 'keyword': keyword}
        print("hello")
        # context = {'videos': top10, 'keyword': keyword}
        return render(request, 'show.html', context)
    if option2 == 'upload' and option4 == 'per-month' and option3=='1to3hr':
        print("hello per-month")
        res = getsearch_detials(youtube, keyword)

        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)

        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials2(youtube, video_ids, all_urls)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released

        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])

        for i in range(len(video_data)):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)

        for i in range(len(video_data)):
            delta = today - dat[i]
            Months = delta.days / 30.44
            months1.append(Months)
        for i in range(len(video_data)):
            if months1[i] == 0:
                months1[i] = 1
            li = months1[i], views[0][i], comments[0][i]
            mperdayviews = views[0][i] / months1[i]
            mperdaycom = comments[0][i] / months1[i]
            mperdaylike = likes[0][i] / months1[i]
            final.append(li)
            mperdayl.append(mperdaylike)
            mperdaysv.append(mperdayviews)
            mperdaysc.append(mperdaycom)

        print(sliderValuee)
        print(sliderValuee1)
        print(sliderValuee2)

        tot1 = sliderValuee + sliderValuee1 + sliderValuee2
        print(tot1)
        if tot1 == 1:
            print("if")
            for i in range(len(video_data)):
                tot = int(
                    (mperdaysv[i] * sliderValuee) + (mperdaysc[i] * sliderValuee1) + (mperdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        # top10
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)
        context = {'videos': video, 'keyword': keyword}
        print("hello")
        # context = {'videos': top10, 'keyword': keyword}
        return render(request, 'show.html', context)
    if option2 == 'upload' and option4 == 'per-month' and option3=='above3':
        print("hello per-month")
        res = getsearch_detials(youtube, keyword)

        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)

        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials3(youtube, video_ids, all_urls)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released

        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])

        for i in range(len(video_data)):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)

        for i in range(len(video_data)):
            delta = today - dat[i]
            Months = delta.days / 30.44
            months1.append(Months)
        for i in range(len(video_data)):
            if months1[i] == 0:
                months1[i] = 1
            li = months1[i], views[0][i], comments[0][i]
            mperdayviews = views[0][i] / months1[i]
            mperdaycom = comments[0][i] / months1[i]
            mperdaylike = likes[0][i] / months1[i]
            final.append(li)
            mperdayl.append(mperdaylike)
            mperdaysv.append(mperdayviews)
            mperdaysc.append(mperdaycom)

        print(sliderValuee)
        print(sliderValuee1)
        print(sliderValuee2)

        tot1 = sliderValuee + sliderValuee1 + sliderValuee2
        print(tot1)
        if tot1 == 1:
            print("if")
            for i in range(len(video_data)):
                tot = int(
                    (mperdaysv[i] * sliderValuee) + (mperdaysc[i] * sliderValuee1) + (mperdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        # top10
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)
        context = {'videos': video, 'keyword': keyword}
        print("hello")
        # context = {'videos': top10, 'keyword': keyword}
        return render(request, 'show.html', context)
    elif option2 == 'upload' and option4 == 'per-year' and option3=='ten':
        print("hello")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials1(youtube, video_ids, all_urls,600)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])
        print("hello")
        for i in range(len(video_data)):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)
        for i in range(len(video_data)):
            delta = today - dat[i]
            years = delta.days / 365.25
            years1.append(years)
        for i in range(len(video_data)):
            if years1[i] == 0:
                years1[i] = 1
            yperdayviews = views[0][i] / years1[i]
            yperdaycom = comments[0][i] / years1[i]
            yperdaylike = likes[0][i] / years1[i]
            yperdayl.append(yperdaylike)
            yperdaysv.append(yperdayviews)
            yperdaysc.append(yperdaycom)

        if sliderValuee + sliderValuee1 + sliderValuee2 == 1:
            for i in range(len(video_data)):
                tot = int(
                    (yperdaysv[i] * sliderValuee) + (yperdaysc[i] * sliderValuee1) + (yperdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }
            video.append(video_dict)

        context = {'videos': video, 'keyword': keyword}
        print("hello")

        return render(request, 'show.html', context)
    elif option2 == 'upload' and option4 == 'per-year' and option3=='one hr':
        print("hello")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials1(youtube, video_ids, all_urls,3600)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])
        print("hello")
        for i in range(len(video_data)):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)
        for i in range(len(video_data)):
            delta = today - dat[i]
            years = delta.days / 365.25
            years1.append(years)
        for i in range(len(video_data)):
            if years1[i] == 0:
                years1[i] = 1
            yperdayviews = views[0][i] / years1[i]
            yperdaycom = comments[0][i] / years1[i]
            yperdaylike = likes[0][i] / years1[i]
            yperdayl.append(yperdaylike)
            yperdaysv.append(yperdayviews)
            yperdaysc.append(yperdaycom)

        if sliderValuee + sliderValuee1 + sliderValuee2 == 1:
            for i in range(len(video_data)):
                tot = int(
                    (yperdaysv[i] * sliderValuee) + (yperdaysc[i] * sliderValuee1) + (yperdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }
            video.append(video_dict)

        context = {'videos': video, 'keyword': keyword}
        print("hello")

        return render(request, 'show.html', context)
    elif option2 == 'upload' and option4 == 'per-year' and option3=='1to3hr':
        print("hello")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials2(youtube, video_ids, all_urls)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])
        print("hello")
        for i in range(len(video_data)):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)
        for i in range(len(video_data)):
            delta = today - dat[i]
            years = delta.days / 365.25
            years1.append(years)
        for i in range(len(video_data)):
            if years1[i] == 0:
                years1[i] = 1
            yperdayviews = views[0][i] / years1[i]
            yperdaycom = comments[0][i] / years1[i]
            yperdaylike = likes[0][i] / years1[i]
            yperdayl.append(yperdaylike)
            yperdaysv.append(yperdayviews)
            yperdaysc.append(yperdaycom)

        if sliderValuee + sliderValuee1 + sliderValuee2 == 1:
            for i in range(len(video_data)):
                tot = int(
                    (yperdaysv[i] * sliderValuee) + (yperdaysc[i] * sliderValuee1) + (yperdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }
            video.append(video_dict)

        context = {'videos': video, 'keyword': keyword}
        print("hello")

        return render(request, 'show.html', context)
    elif option2 == 'upload' and option4 == 'per-year' and option3=='above3':
        print("hello")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials3(youtube, video_ids, all_urls)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])
        print("hello")
        for i in range(len(video_data)):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)
        for i in range(len(video_data)):
            delta = today - dat[i]
            years = delta.days / 365.25
            years1.append(years)
        for i in range(len(video_data)):
            if years1[i] == 0:
                years1[i] = 1
            yperdayviews = views[0][i] / years1[i]
            yperdaycom = comments[0][i] / years1[i]
            yperdaylike = likes[0][i] / years1[i]
            yperdayl.append(yperdaylike)
            yperdaysv.append(yperdayviews)
            yperdaysc.append(yperdaycom)

        if sliderValuee + sliderValuee1 + sliderValuee2 == 1:
            for i in range(len(video_data)):
                tot = int(
                    (yperdaysv[i] * sliderValuee) + (yperdaysc[i] * sliderValuee1) + (yperdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }
            video.append(video_dict)

        context = {'videos': video, 'keyword': keyword}
        print("hello")

        return render(request, 'show.html', context)
    elif option3 == 'ten':
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)

        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials(youtube, video_ids, all_urls)
        video_data = pd.DataFrame(video_detials)
        print(video_data)

        filtered_rows = []

        for i in video_data['Duration']:
            duration = i
            # Parse the duration string using a regular expression
            match = re.search(r"PT(\d+H)?(\d+M)?(\d+S)", duration)
            # Check if the regular expression matched the duration string
            if match:
                # Extract the duration components from the match object
                hours = int(match.group(1)[:-1]) if match.group(1) else 0
                minutes = int(match.group(2)[:-1]) if match.group(2) else 0
                seconds = int(match.group(3)[:-1]) if match.group(3) else 0
                # Calculate the total duration in seconds
                total_seconds = hours * 3600 + minutes * 60 + seconds
                # Print the duration if it is less than 30 minutes
                if total_seconds < 600:
                    filtered_rows.append(True)
                    # print(f"Duration of video {item['id']}: {total_seconds} seconds")
                    # print(f"{i}"+" ")
                else:
                    filtered_rows.append(False)
                    # print(f"Error: could not parse duration string for video ")
            else:
                filtered_rows.append(False)
                # print("error")

        filtered_video_data = video_data.loc[filtered_rows]

        top10 = filtered_video_data
        # top10
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)

        context = {'videos': video, 'keyword': keyword}
        print("hello")
        # context = {'videos': top10, 'keyword': keyword}
        return render(request, 'show.html', context)

    elif option3 == 'one hr':
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)

        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials(youtube, video_ids, all_urls)
        video_data = pd.DataFrame(video_detials)
        print(video_data)

        filtered_rows = []

        for i in video_data['Duration']:
            duration = i
            # Parse the duration string using a regular expression
            match = re.search(r"PT(\d+H)?(\d+M)?(\d+S)", duration)
            # Check if the regular expression matched the duration string
            if match:
                # Extract the duration components from the match object
                hours = int(match.group(1)[:-1]) if match.group(1) else 0
                minutes = int(match.group(2)[:-1]) if match.group(2) else 0
                seconds = int(match.group(3)[:-1]) if match.group(3) else 0
                # Calculate the total duration in seconds
                total_seconds = hours * 3600 + minutes * 60 + seconds
                # Print the duration if it is less than 30 minutes
                if 500 <= total_seconds <= 3600:
                    filtered_rows.append(True)
                    # print(f"Duration of video {item['id']}: {total_seconds} seconds")
                    # print(f"{i}"+" ")
                else:
                    filtered_rows.append(False)
                    # print(f"Error: could not parse duration string for video ")
            else:
                filtered_rows.append(False)
                # print("error")

        filtered_video_data = video_data.loc[filtered_rows]

        top10 = filtered_video_data
        # top10
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)

        context = {'videos': video, 'keyword': keyword}
        # print("hello")
        # context = {'videos': top10, 'keyword': keyword}
        return render(request, 'show.html', context)

    elif option3 == '1to3hr':
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)

        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials(youtube, video_ids, all_urls)
        video_data = pd.DataFrame(video_detials)
        print(video_data)

        filtered_rows = []

        for i in video_data['Duration']:
            duration = i
            # Parse the duration string using a regular expression
            match = re.search(r"PT(\d+H)?(\d+M)?(\d+S)", duration)
            # Check if the regular expression matched the duration string
            if match:
                # Extract the duration components from the match object
                hours = int(match.group(1)[:-1]) if match.group(1) else 0
                minutes = int(match.group(2)[:-1]) if match.group(2) else 0
                seconds = int(match.group(3)[:-1]) if match.group(3) else 0
                # Calculate the total duration in seconds
                total_seconds = hours * 3600 + minutes * 60 + seconds
                # Print the duration if it is less than 30 minutes
                if 3600 <= total_seconds <= 10800:
                    filtered_rows.append(True)
                    # print(f"Duration of video {item['id']}: {total_seconds} seconds")
                    # print(f"{i}"+" ")
                else:
                    filtered_rows.append(False)
                    # print(f"Error: could not parse duration string for video ")
            else:
                filtered_rows.append(False)
                # print("error")

        filtered_video_data = video_data.loc[filtered_rows]

        top10 = filtered_video_data
        # top10
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)

        context = {'videos': video, 'keyword': keyword}
        # print("hello")
        # context = {'videos': top10, 'keyword': keyword}
        return render(request, 'show.html', context)

    if option2 == 'upload' and option4 == 'per-month':
        print("hello per-month")
        res = getsearch_detials(youtube, keyword)

        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)

        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials(youtube, video_ids, all_urls)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released

        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])

        for i in range(0, 50):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)

        for i in range(0, 50):
            delta = today - dat[i]
            Months = delta.days / 30.44
            months1.append(Months)
        for i in range(0, 50):
            if months1[i] == 0:
                months1[i] = 1
            li = months1[i], views[0][i], comments[0][i]
            mperdayviews = views[0][i] / months1[i]
            mperdaycom = comments[0][i] / months1[i]
            mperdaylike = likes[0][i] / months1[i]
            final.append(li)
            mperdayl.append(mperdaylike)
            mperdaysv.append(mperdayviews)
            mperdaysc.append(mperdaycom)

        print(sliderValuee)
        print(sliderValuee1)
        print(sliderValuee2)

        tot1 = sliderValuee + sliderValuee1 + sliderValuee2
        print(tot1)
        if tot1 == 1:
            print("if")
            for i in range(0, 50):
                tot = int(
                    (mperdaysv[i] * sliderValuee) + (mperdaysc[i] * sliderValuee1) + (mperdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        # top10
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)
        context = {'videos': video, 'keyword': keyword}
        print("hello")
        # context = {'videos': top10, 'keyword': keyword}
        return render(request, 'show.html', context)

    elif option2 == 'upload' and option4 == 'per-day':
        print("hello PER-DAY")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials(youtube, video_ids, all_urls)
        print("hello")
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])
        print("hello")
        for i in range(0, 50):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)
        for i in range(0, 50):
            day = (today) - (dat[i])
            day = day.days
            days1.append(day)
        for i in range(0, 50):
            if days1[i] == 0:
                days1[i] = 1
            perdayviews = views[0][i] / days1[i]
            perdaycom = comments[0][i] / days1[i]
            perdaylike = likes[0][i] / days1[i]
            perdayl.append(perdaylike)
            perdaysv.append(perdayviews)
            perdaysc.append(perdaycom)

        if sliderValuee + sliderValuee1 + sliderValuee2 == 1:
            print("upload per-day")
            for i in range(0, 50):
                tot = int((perdaysv[i] * sliderValuee) + (perdaysc[i] * sliderValuee1) + (perdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }

            video.append(video_dict)
        context = {'videos': video, 'keyword': keyword}
        print("hello")

        return render(request, 'show.html', context)

    elif option2 == 'upload' and option4 == 'per-year':
        print("hello")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials(youtube, video_ids, all_urls)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        date1.append(pd.to_datetime(video_data['Published_date']).dt.day)
        month.append(pd.to_datetime(video_data['Published_date']).dt.month)
        year.append(pd.to_datetime(video_data['Published_date']).dt.year)
        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])
        print("hello")
        for i in range(0, 50):
            all = date(year[0][i], month[0][i], date1[0][i])
            dat.append(all)
        for i in range(0, 50):
            delta = today - dat[i]
            years = delta.days / 365.25
            years1.append(years)
        for i in range(0, 50):
            if years1[i] == 0:
                years1[i] = 1
            yperdayviews = views[0][i] / years1[i]
            yperdaycom = comments[0][i] / years1[i]
            yperdaylike = likes[0][i] / years1[i]
            yperdayl.append(yperdaylike)
            yperdaysv.append(yperdayviews)
            yperdaysc.append(yperdaycom)

        if sliderValuee + sliderValuee1 + sliderValuee2 == 1:
            for i in range(0, 50):
                tot = int(
                    (yperdaysv[i] * sliderValuee) + (yperdaysc[i] * sliderValuee1) + (yperdayl[i] * sliderValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }
            video.append(video_dict)

        context = {'videos': video, 'keyword': keyword}
        print("hello")

        return render(request, 'show.html', context)

    elif option2 == 'rating':
        # customdetails.clear()

        print("hello rating")
        res = getsearch_detials(youtube, keyword)
        for i in res['items']:
            video_ids.append(i['id']['videoId'])
        for vid in video_ids:
            all_urls.append("https://www.youtube.com/watch?v=" + vid)
        print("hello")
        # Getting the channel detials of the videos which are the result of our searched keyword
        today = date.today()
        # getting the details of the videos which were the result of the searched keyword

        video_detials = get_video_detials(youtube, video_ids, all_urls)
        video_data = pd.DataFrame(video_detials)
        video_data['Views'] = pd.to_numeric(video_data['Views'])
        video_data['LikeCount'] = pd.to_numeric(video_data['LikeCount'])
        video_data['Comments'] = pd.to_numeric(video_data['Comments'])
        video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date

        views.append(video_data['Views'])
        comments.append(video_data['Comments'])
        likes.append(video_data['LikeCount'])

        # Getting the number of views and comments per day and number of days before the video was released
        print("hello")
        print(sliderrValue)
        print(sliderrValue1)
        print(sliderrValue2)

        if sliderrValuee + sliderrValuee1 + sliderrValuee2 == 1:
            for i in range(0, 50):
                tot = int(
                    (views[0][i] * sliderrValuee) + (comments[0][i] * sliderrValuee1) + (likes[0][i] * sliderrValuee2))
                customdetails.append(tot)

        video_data['CustomSearchResult'] = customdetails
        top10 = video_data.sort_values(by='CustomSearchResult', ascending=False)
        video = []
        for i in top10.index:
            video_url = top10.loc[i, "Url"]

            # Split the video URL by the "=" sign
            split_url = video_url.split("=")

            # Get the last element of the split URL, which should be the video ID
            video_id = split_url[-1]

            video_dict = {
                'link': f'https://www.youtube.com/embed/{video_id}',
                'title': top10.loc[i, 'Video_title'],
                'views': int(top10.loc[i, 'Views']),
                'comments': int(top10.loc[i, 'Comments']),
                'likes': int(top10.loc[i, 'LikeCount']),
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }
            video.append(video_dict)

        # print(video)
        context = {'videos': video, 'keyword': keyword}

        return render(request, 'show.html', context)

    else:
        latest_video = SearchModel.objects.latest('id')
        videos = get_related_videos(latest_video)
        context = {'videos': videos, 'keyword': latest_video.keyword}
        return render(request, 'show.html', context)


def get_related_videos(latest_video):
    # api_key = 'AIzaSyCvUl9TOkkkB_p-NoE5sFYyUa1s7Cmpg5E';  # youtube's api key
    # youtube = build('youtube', 'v3', developerKey=api_key)
    search_response = youtube.search().list(q=latest_video.keyword, part='id', type='video', maxResults=10).execute()
    video_ids = [search_result['id']['videoId'] for search_result in search_response.get('items', [])]

    # Get video details using videos API
    video_response = youtube.videos().list(id=','.join(video_ids), part='snippet,statistics').execute()
    videos = [{
        'link': f'https://www.youtube.com/embed/{video["id"]}',
        'title': video['snippet']['title'],
        'views': int(video['statistics']['viewCount']),
        'url': f'https://www.youtube.com/watch?v={video["id"]}',
        'comments': int(video['statistics']['commentCount']),
        'likes': int(video['statistics']['likeCount']),
    } for video in video_response.get('items', [])]
    return videos


def getsearch_detials(youtube, keyword):
    request = youtube.search().list(q=keyword, part='snippet,id', type='video',
                                    maxResults=30)  # using youtube's inbuild function to get the list of vidoes of the searched keyword
    response = request.execute()
    return response  # We get the response in json format


def get_video_detials(youtube, video_ids, all_urls):
    all_video = []
    if not video_ids:
        return "No video IDs provided."

    if len(video_ids) > 50:
        return "Too many video IDs. Maximum number of video IDs is 50."

    request = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=','.join(video_ids)
    )
    # Here we use the youtube's api inbuilt function to get the information about the number of
    # views,comments and all other related information
    response = request.execute()
    for vid, video in zip(all_urls, response['items']):
        duration = video['contentDetails']['duration']
        # duration = duration.replace('PT', ':').replace('D', ':').replace('H', ':').replace('M', ':').replace('S', '')
        # duration = ':'.join([i.zfill(2) for i in duration.split(':')])
        video_data = dict(Url=vid, Video_title=video['snippet']['title'], Views=video['statistics']['viewCount'],
                          LikeCount=int(video['statistics'].get('likeCount', 0)),
                          Comments=int(video['statistics'].get('commentCount', 0)),
                          Channel_id=video['snippet']['channelId'], Published_date=video['snippet']['publishedAt'],
                          Duration=duration)
        all_video.append(video_data)
    return all_video

def get_video_detials1(youtube, video_ids, all_urls,time):
    all_video = []
    if not video_ids:
        return "No video IDs provided."

    if len(video_ids) > 50:
        return "Too many video IDs. Maximum number of video IDs is 50."

    request = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=','.join(video_ids)
    )
    # Here we use the youtube's api inbuilt function to get the information about the number of
    # views,comments and all other related information
    response = request.execute()
    for vid, video in zip(all_urls, response['items']):
        duration = video['contentDetails']['duration']
        duration_secs = duration_to_seconds(duration)
        if duration_secs > time:
            continue
        video_data = {
            'Url': vid,
            'Video_title': video['snippet']['title'],
            'Views': int(video['statistics']['viewCount']),
            'LikeCount': int(video['statistics'].get('likeCount', 0)),
            'Comments': int(video['statistics'].get('commentCount', 0)),
            'Channel_id': video['snippet']['channelId'],
            'Published_date': video['snippet']['publishedAt'],
            'Duration': duration
        }
        all_video.append(video_data)
    return all_video
def get_video_detials2(youtube, video_ids, all_urls):
    all_video = []
    if not video_ids:
        return "No video IDs provided."

    if len(video_ids) > 50:
        return "Too many video IDs. Maximum number of video IDs is 50."

    request = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=','.join(video_ids)
    )
    # Here we use the youtube's api inbuilt function to get the information about the number of
    # views,comments and all other related information
    response = request.execute()
    for vid, video in zip(all_urls, response['items']):
        duration = video['contentDetails']['duration']
        duration_secs = duration_to_seconds(duration)
        if duration_secs < 3600 and duration_secs < 10800:
            continue
        video_data = {
            'Url': vid,
            'Video_title': video['snippet']['title'],
            'Views': int(video['statistics']['viewCount']),
            'LikeCount': int(video['statistics'].get('likeCount', 0)),
            'Comments': int(video['statistics'].get('commentCount', 0)),
            'Channel_id': video['snippet']['channelId'],
            'Published_date': video['snippet']['publishedAt'],
            'Duration': duration
        }
        all_video.append(video_data)
    return all_video
def get_video_detials3(youtube, video_ids, all_urls):
    all_video = []
    if not video_ids:
        return "No video IDs provided."

    if len(video_ids) > 50:
        return "Too many video IDs. Maximum number of video IDs is 50."

    request = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=','.join(video_ids)
    )
    # Here we use the youtube's api inbuilt function to get the information about the number of
    # views,comments and all other related information
    response = request.execute()
    for vid, video in zip(all_urls, response['items']):
        duration = video['contentDetails']['duration']
        duration_secs = duration_to_seconds(duration)
        if duration_secs > 10800:
            continue
        video_data = {
            'Url': vid,
            'Video_title': video['snippet']['title'],
            'Views': int(video['statistics']['viewCount']),
            'LikeCount': int(video['statistics'].get('likeCount', 0)),
            'Comments': int(video['statistics'].get('commentCount', 0)),
            'Channel_id': video['snippet']['channelId'],
            'Published_date': video['snippet']['publishedAt'],
            'Duration': duration
        }
        all_video.append(video_data)
    return all_video

def duration_to_seconds(duration):
    duration = duration.replace('PT', '')
    seconds = 0
    if 'H' in duration:
        hours, duration = duration.split('H')
        seconds += int(hours) * 3600
    if 'M' in duration:
        minutes, duration = duration.split('M')
        seconds += int(minutes) * 60
    if 'S' in duration:
        seconds += int(duration[:-1])
    return seconds

import re
import pandas as pd


#
# def parse_duration(duration):
#     """
#     Parse a duration string in ISO 8601 format (e.g. PT10M30S) into a pandas timedelta object.
#     """
#     match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
#     if match:
#         hours = int(match.group(1)[:-1]) if match.group(1) else 0
#         minutes = int(match.group(2)[:-1]) if match.group(2) else 0
#         seconds = int(match.group(3)[:-1]) if match.group(3) else 0
#         return pd.Timedelta(hours=hours, minutes=minutes, seconds=seconds)
#     else:
#         return pd.NaT


def show(request):
    # Get latest video from database
    latest_video = SearchModel.objects.latest('id')

    # Process latest video data using the YouTube API
    video = get_related_videos(latest_video)

    # Create context dictionary to pass to template
    context = {
        'video': video,
        'keyword': latest_video.keyword
    }

    return render(request, 'show.html', context)


# analyse videos
def analyse_video(request):
    if request.method == 'GET':
        video_url = request.GET.get('video_url')
        # api_key = 'AIzaSyCvUl9TOkkkB_p-NoE5sFYyUa1s7Cmpg5E'
        # youtube = build('youtube', 'v3', developerKey=api_key)
        print(video_url)
        video_id = video_url.split('=')[1]
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
        return JsonResponse(result)


def showPlaylist(request):
    return render(request, "playlist_result.html")


def showChannel(request):
    return render(request, "chan.html")


def Channel(request):
    return render(request, "Channel.html")


def Video(request):
    return render(request, "Video.html")


def cmpc(request):
    return render(request, "cmpc.html")


def cmpv(request):
    return render(request, "cmpv.html")


@login_required
def home(request):
    return render(request, 'home.html')


def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            print("user none")
            messages.success(request, 'User not found.')
            return redirect('/accounts/login')

        if user_obj is not None:
            profile_obj = Profile.objects.filter(user=user_obj).first()
            if profile_obj is not None and not profile_obj.is_verified:
                messages.success(request, 'Profile is not verified. Please check your email.')
                return redirect('/accounts/login')
        else:
            messages.success(request, 'User not found.')
            return redirect('/accounts/login')
            # messages.success(request, 'Profile is not verified check your mail.')
            # return redirect('/accounts/login')
        # if not profile_obj.is_verified and user_obj is None:
        # if user_obj is not None and not profile_obj.is_verified:

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/accounts/login')

        login(request, user)
        return redirect('/')

    return render(request, 'login.html')


def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)
        print(email)

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            print(auth_token)
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token, email=email)
            profile_obj.save()
            print(auth_token)
            print(user_obj.username)

            # send_mail_after_registration(email, auth_token)
            send_mail_to_all(request, user_obj.email, auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, 'register.html')


def auth_t(auth_token):
    token = auth_token


def success(request):
    return render(request, 'success.html')


def token_send(request):
    return render(request, 'token_send.html')


def send_mail_to_all(request, user_email, auth_token):
    # print(auth_token)
    print(user_email)
    print(auth_token)
    send_mail_func.delay(user_email, auth_token)
    return HttpResponse("Sent")


def error_page(request):
    return render(request, 'error.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')


def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('/')


# def forget(request):
#     return render(request, 'forget-password.html')


# def change(request):
#     return render(request, 'change-password.html')


def change_password(request, token):
    context = {}
    print(token)
    profile_obj = Profile1.objects.filter(forget_password_token=token).first()
    context = {'user_id': profile_obj.user.id}
    # print(profile_obj)
    try:
        if request.method == 'POST':
            new_pass = request.POST.get('new_password')
            confirm_pass = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')
            print(new_pass)
            print(confirm_pass)

            if user_id is None:
                messages.success(request, 'No user id found')
                return redirect(f'/change-password/{token}/')

            if new_pass != confirm_pass:
                messages.success(request, 'both passwords should be equal')
                return redirect(f'/change-password/{token}/')

            user_obj = User.objects.get(id=user_id)
            print(user_obj)
            user_obj.set_password(new_pass)
            user_obj.save()
            return redirect('/accounts/login/')

    except Exception as e:
        print(e)
    return render(request, 'change-password.html', context)


def forget_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            print(username)
            # if User.objects.filter(username=username).first():
            #     messages.success(request, 'Username is not found.')
            #     return redirect('/forget-password')
            user_obj = User.objects.get(username=username)
            profile_obj = Profile1();
            # if profile_obj.user is None:
            #     messages.success(request, 'No user id found')
            #     return redirect('/forget-password')
            # print(user_obj)
            token = str(uuid.uuid4())
            print(token)
            # print(user_obj.email)
            # profile_obj = Profile1.objects.get(user=user_obj,forget_password_token = token,email = email)
            # # profile_obj.forget_password_token = token
            # profile_obj.save()
            print(username)

            profile_obj.user = user_obj;
            profile_obj.forget_password_token = token;
            profile_obj.save();
            print(profile_obj.forget_password_token)
            send_forget_password_mail(request, user_obj.email, profile_obj.forget_password_token)
            messages.success(request, 'An Email is sent.')
            return redirect('/forget-password')
        return render(request, 'forget-password.html')
    except Exception as e:
        print(e)
        return render(request, 'forget-password.html')


def send_forget_password_mail(request, email1, token):
    print(token)
    send_mail_forget.delay(email1, token)
    return HttpResponse("Done")

# subject = "Your forget password link" message = f'Hi, click one the link to reset your password
# http://127.0.0.1:8000/http://127.0.0.1:8000/change-password/{token}/ ' email_from = settings.EMAIL_HOST_USER
# recipient_list = [email1] send_mail(subject, message, email_from, recipient_list) return True



# playlist filter





def update_result1(request):
    print("hi")
    option1 = request.POST.get("two")
    option2 = request.POST.get("three")
    print(option1)
    print(option2)
    latest_video = SearchModel.objects.latest('id')
    keyword = latest_video.keyword
    if(option1=='ViewCount' and option2=='1to5hr'):
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            if playlist.time < 18000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        sorted_data = sorted(playlist_data, key=lambda x: x['view_count'], reverse=True)

        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    if(option1=='ViewCount' and option2=='ten'):
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            print(playlist.time)
            if playlist.time < 36000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        sorted_data = sorted(playlist_data, key=lambda x: x['view_count'], reverse=True)

        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    if(option1=='ViewCount' and option2=='twenty'):
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            if playlist.time < 72000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        sorted_data = sorted(playlist_data, key=lambda x: x['view_count'], reverse=True)

        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    if(option1=='ViewCount' and option2=='20more'):
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            if playlist.time > 72000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        sorted_data = sorted(playlist_data, key=lambda x: x['view_count'], reverse=True)

        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    elif(option1=='Standard Deviation' and option2=='1to5hr'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            if playlist.time < 18000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'std':playlist.se,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        sorted_data = sorted(playlist_data, key=lambda x: x['std'], reverse=False)

        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'standard_deviation':playlist['std'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    elif(option1=='Standard Deviation' and option2=='ten'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            if playlist.time < 36000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'std':playlist.se,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        sorted_data = sorted(playlist_data, key=lambda x: x['std'], reverse=False)

        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'standard_deviation':playlist['std'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    elif(option1=='Standard Deviation' and option2=='twenty'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            if playlist.time < 72000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'std':playlist.se,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        sorted_data = sorted(playlist_data, key=lambda x: x['std'], reverse=False)

        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'standard_deviation':playlist['std'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    elif(option1=='Standard Deviation' and option2=='20more'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            if playlist.time > 72000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'std':playlist.se,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        sorted_data = sorted(playlist_data, key=lambda x: x['std'], reverse=False)

        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'standard_deviation':playlist['std'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    elif(option1=='Views to Video Ratio' and  option2=='1to5hr'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            if playlist.time < 18000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'video_count': playlist.vc,
                    'std':playlist.se,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        sorted_data = sorted(playlist_data, key=lambda x: x['view_count']/(x['video_count'] or float('inf')), reverse=True)
        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    elif(option1=='Views to Video Ratio' and  option2=='ten'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            if playlist.time < 36000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'video_count': playlist.vc,
                    'std':playlist.se,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        sorted_data = sorted(playlist_data, key=lambda x: x['view_count']/(x['video_count'] or float('inf')), reverse=True)
        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    elif(option1=='Views to Video Ratio' and  option2=='twenty'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            if playlist.time < 72000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'video_count': playlist.vc,
                    'std':playlist.se,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        sorted_data = sorted(playlist_data, key=lambda x: x['view_count']/(x['video_count'] or float('inf')), reverse=True)
        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    elif(option1=='Views to Video Ratio' and  option2=='20more'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            if playlist.time > 72000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'video_count': playlist.vc,
                    'std':playlist.se,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        sorted_data = sorted(playlist_data, key=lambda x: x['view_count']/(x['video_count'] or float('inf')), reverse=True)
        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})

    elif(option1=='ViewCount'):
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            playlist_data.append({
                'playlist_id': playlist.pid,
                'title': playlist.title,
                'view_count': playlist.view_count,
                'hours':playlist.hours,
                'minutes':playlist.minutes
            })
        sorted_data = sorted(playlist_data, key=lambda x: x['view_count'], reverse=True)

        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})

    elif(option1=='Standard Deviation'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            playlist_data.append({
                'playlist_id': playlist.pid,
                'title': playlist.title,
                'view_count': playlist.view_count,
                'std':playlist.se,
                'hours':playlist.hours,
                'minutes':playlist.minutes
            })
        sorted_data = sorted(playlist_data, key=lambda x: x['std'], reverse=False)

        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'standard_deviation':playlist['std'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    elif(option1=='Views to Video Ratio'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            playlist_data.append({
                'playlist_id': playlist.pid,
                'title': playlist.title,
                'view_count': playlist.view_count,
                'video_count': playlist.vc,
                'std':playlist.se,
                'hours':playlist.hours,
                'minutes':playlist.minutes
            })
        sorted_data = sorted(playlist_data, key=lambda x: x['view_count']/(x['video_count'] or float('inf')), reverse=True)
        playlist_dict = {}
        for i, playlist in enumerate(sorted_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})

    elif(option2=='20more'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query :
            if playlist.time>72000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'video_count': playlist.vc,
                    'std':playlist.se,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        playlist_dict = {}
        for i, playlist in enumerate(playlist_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    elif(option2=='twenty'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query :
            if playlist.time<72000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'video_count': playlist.vc,
                    'std':playlist.se,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        playlist_dict = {}
        for i, playlist in enumerate(playlist_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request,'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    elif(option2=='ten'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query:
            if playlist.time < 36000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'video_count': playlist.vc,
                    'std':playlist.se,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        playlist_dict = {}
        for i, playlist in enumerate(playlist_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})
    elif(option2=='1to5'):
        # Save keyword to database
        playlist_query = Playlist.objects.filter(keyword=keyword)
        playlist_data = []
        for playlist in playlist_query :
            print(playlist.time)
            if playlist.time<18000:
                playlist_data.append({
                    'playlist_id': playlist.pid,
                    'title': playlist.title,
                    'view_count': playlist.view_count,
                    'video_count': playlist.vc,
                    'std':playlist.se,
                    'hours':playlist.hours,
                    'minutes':playlist.minutes
                })
        playlist_dict = {}
        for i, playlist in enumerate(playlist_data):
            playlist_dict[playlist['playlist_id']] = {
                'playlist_id': playlist['playlist_id'],
                'title': playlist['title'],
                'view_count': playlist['view_count'],
                'hours':playlist['hours'],
                'minutes':playlist['minutes']
            }
        return render(request, 'playlist_result.html', {'playlists': playlist_dict, 'keyword':keyword})



