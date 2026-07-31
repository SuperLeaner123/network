from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    path("post/", views.create_post, name="create_post"),
    path("following/", views.following_feed, name="following"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),

    path("like/<int:post_id>/", views.toggle_like, name="toggle_like"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
]
