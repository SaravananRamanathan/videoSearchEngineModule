"""
in here we gooan define paths
to select for respective view
"""
from django.urls import path
from . import views
#starting page path with ""
urlpatterns = [
    path("",views.infoPage, name="info"),#info page.
    path("video-search-answer/",views.videoSearchAnswer,name="video-search-answer"),
]
