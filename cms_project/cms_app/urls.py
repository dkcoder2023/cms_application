from django.urls import path
from .views import LoginView, CreateUserView, ReadUpdateDeleteUserView, CreatePostView, ReadUpdateDeletePostView, \
    CreateLikeView, ReadUpdateDeleteLikeView,RetriveallUserView,RetriveAllPostView,RetriveallLikeView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', CreateUserView.as_view(), name='create_user'),
    path('getallusers/', RetriveallUserView.as_view(), name='get_alluser_detail'),
    path('users/<int:user_id>/', ReadUpdateDeleteUserView.as_view(), name='user_detail'),
    path('posts/', CreatePostView.as_view(), name='create_post'),
    path('posts/<int:post_id>/', ReadUpdateDeletePostView.as_view(), name='post_detail'),
    path('getallpost/', RetriveAllPostView.as_view(), name='get_all_post'),
    path('likes/', CreateLikeView.as_view(), name='create_like'),
    path('getalllikes/', RetriveallLikeView.as_view(), name='get_all_like'),
    path('likes/<int:like_id>/', ReadUpdateDeleteLikeView.as_view(), name='like_detail'),   
] 