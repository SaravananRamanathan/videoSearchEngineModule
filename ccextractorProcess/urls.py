"""
in here we gooan define paths
to select for respective view
"""
from django.urls import path
from . import views
#starting page path with ""
urlpatterns = [
    path("",views.homePage, name="home"),#home page
    path("uploadButton/",views.uploadButton,name="uploadButton")
]
