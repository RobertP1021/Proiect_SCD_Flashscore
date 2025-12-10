from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('matches/', views.get_matches),
    path('matches/<int:match_id>/', views.get_match),
    path('matches/event/', views.create_match),
    path('matches/<int:match_id>/update/', views.update_match),
    path('matches/<int:match_id>/delete/', views.delete_match),
    path('subscriptions/<int:match_id>/', views.subscribe_match),
]