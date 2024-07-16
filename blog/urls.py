from django.urls import path
from .views import PostList, PostDetail, PostCreateView

urlpatterns = [
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
]
