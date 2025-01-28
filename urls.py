from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("today/<str:city>/", views.today, name="today"),
    path("search_page/<str:searched_city>/", views.search_page, name="search-page"),
    
]

