from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters

from utils.permissions import IsOwnerOrReadOnly
from .models import Post, Comment
from .serializers import (
    PostCreateSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentCreateSerializer,
)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['description', 'body']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        return PostCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        serializer.save(user=user, post=post)