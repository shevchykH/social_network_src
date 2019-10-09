from django.urls import path

from post.api.views import PostList, PostDetail, PostLike, PostUnlike

urlpatterns = [
    path('api/posts/', PostList.as_view(), name='post_list'),
    path('api/posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('api/posts/<int:pk>/like/', PostLike.as_view(), name='like'),
    path('api/posts/<int:pk>/unlike/', PostUnlike.as_view(), name='unlike'),
]
