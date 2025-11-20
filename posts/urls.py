from django.urls import path

from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.PostListCreateView.as_view(), name='list_create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

    path('<int:pk>/new-comment/', views.CommentCreateView.as_view(), name='new_comment'),
]