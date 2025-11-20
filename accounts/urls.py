from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path('', views.UserListCreateView.as_view(), name='list_create'),
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('<str:username>/follow/', views.FollowView.as_view(), name='follow'),
    path('<str:username>/unfollow/', views.UnfollowView.as_view(), name='unfollow'),
    path('<str:username>/followers/', views.FollowerListView.as_view(), name='follower_list'),
    path('<str:username>/following/', views.FollowingListView.as_view(), name='following_list'),
]