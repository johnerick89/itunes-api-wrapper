from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from music import views

urlpatterns = [
    path('artists/', views.ArtistList.as_view()),
    path('artists/<int:pk>/', views.ArtistDetail.as_view()),
    path('albums/', views.AlbumList.as_view()),
    path('albums/<int:pk>/', views.AlbumDetail.as_view()),
    path('songs/', views.SongList.as_view()),
    path('songs/<int:pk>/', views.SongDetail.as_view()),
    path('seed', views.SeedDataView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)