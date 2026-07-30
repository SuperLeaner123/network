from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User, Post, Follow

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        return render(request, "network/login.html", {"message": "Invalid username or password."})
    return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {"message": "Passwords must match."})
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except:
            return render(request, "network/register.html", {"message": "Username already taken."})
        login(request, user)
        return redirect("index")
    return render(request, "network/register.html")

def paginate(request, posts):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)

@login_required
def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    page_obj = paginate(request, posts)
    return render(request, "network/index.html", {"page_obj": page_obj})


@login_required
def create_post(request):
    if request.method == "POST":
        body = request.POST.get("body", "").strip()
        if body:
            Post.objects.create(user=request.user, body=body)
        return redirect("index")
    return redirect("index")

@login_required
def following_feed(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list("user", flat=True)
    posts = Post.objects.filter(user__in=following_ids).order_by("-timestamp")
    page_obj = paginate(request, posts)
    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "following_ids": following_ids
    })

@login_required
def profile(request, user_id):
    profile_user = User.objects.get(id=user_id)
    posts = Post.objects.filter(user=profile_user).order_by("-timestamp")
    page_obj = paginate(request, posts)
    followers_count = Follow.objects.filter(user=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    is_following = False
    if request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, user=profile_user).exists()
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following
    })

@login_required
def follow_user(request, user_id):
    target = User.objects.get(id=user_id)
    if target != request.user:
        Follow.objects.get_or_create(follower=request.user, user=target)
    return redirect("profile", user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    target = User.objects.get(id=user_id)
    Follow.objects.filter(follower=request.user, user=target).delete()
    return redirect("profile", user_id=user_id)

@login_required
def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect("index")

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.user != request.user:
        return redirect("index")
    if request.method == "POST":
        new_body = request.POST.get("body", "").strip()
        if new_body:
            post.body = new_body
            post.save()
        return redirect("index")
    return render(request, "network/edit.html", {"post": post})
