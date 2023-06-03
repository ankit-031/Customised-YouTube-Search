from django.contrib import admin
from django.urls import path, include
from .views import *
from . import  views

urlpatterns = [
    path('', home, name="home"),
    path('CustomSearch',views.CustomSearch,name="Custom-search"),
    path('Channel',views.Channel,name="Channel"),
    path('Video',views.Video,name="Video"),
    path('cmpc',views.cmpc,name="cmpc"),
    path('cmpv',views.cmpv,name="cmpv"),
    path('register', register_attempt, name="register_attempt"),
    path('accounts/login/', login_attempt, name="login_attempt"),
    path('token', token_send, name="token_send"),
    path('success', success, name='success'),
    path('verify/<auth_token>', verify, name="verify"),
    path('error', error_page, name="error"),
    path('signout', signout, name='signout'),
    path('change-password/<token>/', change_password, name="change-password"),
    path('forget-password/', forget_password, name='forget-password'),
    path('sendmail/', send_mail_to_all, name='sendmail'),
    path('ShowVideo/', showVideo, name='ShowVideo'),
    path('ShowPlaylist/', showPlaylist, name='ShowPlaylist'),
    path('ShowChannel/', showChannel, name='ShowChannel'),
    path('ShowPlaylist/ShowChannel/', showChannel, name='ShowChannel'),
    path('analyse/', views.analyse_video, name='analyse_video'),
    # path('ShowPlaylist/ShowVideo/', showVideo, name='ShowVideo'),
    # path('submit_form/', views.submit_form, name='submit_form'),
    path('show',views.show,name='show'),
    path('ShowVideo/update_result/', views.update_result, name='update_result'),
    path('update_result/', views.update_result, name='update_result'),
    path('aboutUs/', views.about_us, name='about-us'),
    path('update_result1/',views.update_result1,name='update_result1'),
    # path('filtered-videos/', views.filtered_videos, name='filtered_videos'),
    # path('my_view/', views.my_view, name='my_view'),

    # path('forget-password/', forget, name='forget-password'),
]
