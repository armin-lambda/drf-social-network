from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.permissions import (
    IsAnonymous,
    IsNotSelf,
    IsOwnerOrReadOnly
)
from .models import Relation
from .serializers import (
    RegisterSerializer,
    UserListSerializer,
    UserProfileSerializer,
)


User = get_user_model()


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'bio']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAnonymous()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterSerializer
        return UserListSerializer


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = UserProfileSerializer
    lookup_field = 'username'


class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNotSelf]

    def post(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])

        if Relation.objects.filter(from_user=request.user, to_user=user).exists():
            return Response(
                {'detail': 'Followed already.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        Relation.objects.create(from_user=request.user, to_user=user)
        return Response(
            {'detail': 'Followed successfully'},
            status=status.HTTP_201_CREATED,
        )


class UnfollowView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNotSelf]

    def delete(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            relation.delete()
            return Response(
                {'detail': 'Unfollowed successfully'},
                status=status.HTTP_204_NO_CONTENT,
            )
        
        return Response(
            {'detail': 'First follow'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class FollowerListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return user.get_followers()


class FollowingListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserListSerializer
    lookup_field = 'username'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return user.get_following()