from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.post_view, name="all_posts"),
    path("profile/<str:username>", views.profile_view, name="profile"),
    path("like_unlike/<str:id>", views.like_unlike, name="like_unlike"),
    path("follow_unfollow/<str:flag>/<str:user>", views.follow_unfollow, name="follow_unfollow"),
    path("edit/<str:id>", views.edit, name="edit"),
    path("following", views.following, name="following"),
]
