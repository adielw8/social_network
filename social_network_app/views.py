from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from .serializers import PostSerializer, LikeSerializer, UnLikeSerializer, UserSerializer
from .hunter_clearbit import hunter_email_verifier, clearbit_email_data
from .models import Post, Like, UnLike


# create user
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            hunter = hunter_email_verifier(email)
            clearbit = clearbit_email_data(email)
            if hunter:
                if clearbit:
                    serializer.validated_data['first_name'] = clearbit['first_name']
                    serializer.validated_data['last_name'] = clearbit['last_name']
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response({'status': 'EMAIL NOT VERIFIED'})
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)
        Like.objects.create(post=post)
        UnLike.objects.create(post=post)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(generics.GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        post_id = self.request.POST.get('post')
        un_liked_posts = UnLike.objects.get(post_id=post_id)
        liked_posts = Like.objects.get(post_id=post_id)
        if user not in liked_posts.like.all():
            if user in un_liked_posts.un_like.all():
                un_liked_posts.un_like.remove(user)
            liked_posts.like.add(user)
            return Response()
        else:
            liked_posts.like.remove(user)
            return Response()


class UnLikeViewSet(generics.GenericAPIView):
    queryset = UnLike.objects.all()
    serializer_class = UnLikeSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        post_id = self.request.POST.get('post')
        un_liked_posts = UnLike.objects.get(post_id=post_id)
        liked_posts = Like.objects.get(post_id=post_id)

        if user not in un_liked_posts.un_like.all():
            if user in liked_posts.like.all():
                liked_posts.like.remove(user)
            un_liked_posts.un_like.add(user)
            return Response()
        else:
            un_liked_posts.un_like.remove(user)
            return Response()
