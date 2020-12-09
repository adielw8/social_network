from django.urls import path, include
from rest_framework import urls
from .views import PostViewSet, LikeViewSet, UnLikeViewSet, UserCreateAPIView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('post', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/create/', UserCreateAPIView.as_view(), name='create'),
    path('like/', LikeViewSet.as_view()),
    path('unlike/', UnLikeViewSet.as_view()),
    path('api-auth/', include(urls)),

]
