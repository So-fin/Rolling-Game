from .views import *
from django.urls import path

urlpatterns = [
    path('startgame/', startGameView.as_view(), name='startgame'),
    path('roll/<int:gamesession_id>/', rollView.as_view(), name='roll'),
    path('cashout/<int:gamesession_id>/', cashOutView.as_view(), name='cashout'),
]

