from django.urls import path
from . import views

urlpatterns = [
    path('matches/', views.get_matches),
    path('matches/<int:match_id>/', views.get_match),
    path('subscriptions/<int:match_id>/', views.subscribe_match),
]