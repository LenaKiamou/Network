from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


def index(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = NewPost(request.POST)
            if form.is_valid():
                new = form.save(commit=False)
                new.owner = request.user
                new.save()
                return redirect("all_posts")
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        form = NewPost()
    
    posts = Post.objects.all()
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'form': form, 'posts': page_obj}
    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            follow = Follow.objects.create(follower = user)
            follow.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



def post_view (request):
    form = NewPost(request.POST)
    if request.method == "POST":
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.owner = request.user
            newForm.save()

    posts = Post.objects.all()
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    context = { 'post': NewPost(), 'posts': page_obj }
    return render(request, "network/post.html", context)


def profile_view(request, username):
    profile_user = User.objects.get(username=username)
    following = Follow.objects.filter(following=profile_user.id)
    followings = len(following)
    follower = Follow.objects.get(follower=profile_user.id)
    numF = follower.following.count() 

    if request.user.is_authenticated:
        current_user = request.user
        posts = Post.objects.filter(owner=profile_user).all()
    else:
        current_user = None
        posts = Post.objects.filter(owner=profile_user).all()

    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = { 'profileUser': profile_user, 
                'currentUser': current_user,
                'posts': page_obj, 
                'followings': followings,
                'numF': numF,
                'following': following
                }
    return render(request, "network/profile.html", context)      


@csrf_exempt
def like_unlike(request, id):
    post = Post.objects.get(id=id)
    user = User.objects.get(username=request.user.username)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    if request.method == "PUT":
        data = json.loads(request.body)
        
        if data.get("like"):
            post.liked.add(user)
        else:
            post.liked.remove(user)
        post.save()


def follow_unfollow(request, flag, user):
    profile = User.objects.get(username=user)
    user = Follow.objects.get(follower=profile.id)
    if request.user.id != user.id:
        if flag == "follow":
            if user == None or request.user.id not in user.following.all():
                user.following.add(request.user.id)
                num = user.following.count()
                return JsonResponse({"flag": 'follow', "num" : num})

        if flag == "unfollow":
            user.following.remove(request.user.id)
            num = user.following.count()
            return JsonResponse({"flag": 'unfollow', "num" : num})


@login_required
def following(request):
    current_user = User.objects.get(username=request.user.username)
    following = Follow.objects.filter(following=current_user.id)
    print(following)
    user=User.objects.filter(id__in=following)
    posts=Post.objects.filter(owner__in=user)
    
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = { 'posts' : page_obj }
    return render(request, "network/following.html", context)


@csrf_exempt
def edit(request, id):
    post = Post.objects.get(id=id)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("description") is not None:
            post.description = data["description"]
        post.save()
