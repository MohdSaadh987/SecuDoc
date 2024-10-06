# views.py

import json
import base64
from hashlib import sha256
from cryptography.fernet import Fernet
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from fmsApp.forms import UserRegistration, SavePost, UpdateProfile, UpdatePasswords
from fmsApp.models import Post
from hashlib import sha256
from .models import Post
from .forms import PasswordUpdateForm



# Function to hash file content
def hash_file(file_path):
    hasher = sha256()
    with open(file_path, 'rb') as f:
        while True:
            buf = f.read(4096)  # Read file in chunks of 4096 bytes
            if not buf:
                break
            hasher.update(buf)
    return hasher.hexdigest()
# Global context for templates
context = {
    'page_title': 'File Management System',
}

# Login view
def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Account is not active."
        else:
            resp['msg'] = "Invalid username or password."
    return HttpResponse(json.dumps(resp), content_type='application/json')

# Logout view
def logoutuser(request):
    logout(request)
    return redirect('/')

# Home view

@login_required
def home(request):
    context = {'page_title': 'Home'}
    if request.user.is_superuser:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(user=request.user)
    context['posts'] = posts
    context['postsLen'] = posts.count()

    if request.method == 'POST':
        form = PasswordUpdateForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            post.password = form.cleaned_data['password']
            post.save()
            return redirect('home-page')
    else:
        form = PasswordUpdateForm()
    
    context['form'] = form

    return render(request, 'home.html', context)

# User registration view
def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home-page')
    context['page_title'] = "Register User"
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            loginUser = authenticate(username=username, password=password)
            login(request, loginUser)
            return redirect('home-page')
        else:
            context['reg_form'] = form
    else:
        form = UserRegistration()
        context['reg_form'] = form
    return render(request, 'register.html', context)

# User profile view
@login_required
def profile(request):
    context['page_title'] = 'Profile'
    return render(request, 'profile.html', context)

# Manage posts view
@login_required
def posts_mgt(request):
    context['page_title'] = 'Uploads'
    posts = Post.objects.filter(user=request.user).order_by('title', '-date_created')
    context['posts'] = posts
    return render(request, 'posts_mgt.html', context)

# Manage single post view
@login_required
def manage_post(request, pk=None):
    context['page_title'] = 'Manage Post'
    context['post'] = {}
    if pk is not None:
        post = Post.objects.get(id=pk)
        context['post'] = post
    return render(request, 'manage_post.html', context)

# Save or update post view
@login_required
def save_post(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        post_id = request.POST.get('id')
        if post_id:
            post = Post.objects.get(id=post_id)
            form = SavePost(request.POST, request.FILES, instance=post)
        else:
            form = SavePost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            
            # Example of hashing file content if needed:
            if post.file_path:
                post.hashed_content = hash_file(post.file_path.path)
                post.save()

            messages.success(request, 'File has been saved successfully.')
            resp['status'] = 'success'
        else:
            resp['msg'] = form.errors
    else:
        resp['msg'] = "No data sent."
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Delete post view
@login_required
def delete_post(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        post_id = request.POST.get('id')
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            resp['status'] = 'success'
            messages.success(request, 'Post has been deleted successfully')
        except Post.DoesNotExist:
            resp['msg'] = "Post does not exist"
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Share file view
def shareF(request, id=None):
    context = {'page_title': 'Shared File'}
    if id is not None:
        key = settings.ID_ENCRYPTION_KEY
        fernet = Fernet(key)
        id = base64.urlsafe_b64decode(id)
        id = fernet.decrypt(id).decode()
        post = get_object_or_404(Post, id=id)
        
        if request.method == 'POST':
            input_password = request.POST.get('password')
            if post.password and input_password == post.password:
                context['post'] = post
                context['page_title'] += " - " + post.title
                context['file_url'] = post.file_path.url  # Ensure the file URL is accessible from the template
                return render(request, 'share-file.html', context)
            else:
                context['error'] = 'Invalid password'
        else:
            context['post'] = None

    return render(request, 'password_protect.html', context)

# Update user profile view
@login_required
def update_profile(request):
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id=request.user.id)
    if request.method != 'POST':
        form = UpdateProfile(instance=user)
        context['form'] = form
    else:
        form = UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile")
        else:
            context['form'] = form
    return render(request, 'manage_profile.html', context)

# Update user password view
@login_required
def update_password(request):
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = UpdatePasswords(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile")
        else:
            context['form'] = form
    else:
        form = UpdatePasswords(request.POST)
        context['form'] = form
    return render(request, 'update_password.html', context)


def index(request):
    # Replace with your logic to fetch and process data for rendering the index page
    context = {
        'page_title': 'Home',
        'posts': Post.objects.all(),  # Example queryset, adjust as per your models
    }
    return render(request, 'index.html', context)


def topicsdetail(request):
    # Replace with your logic to fetch and process data for rendering the index page
    context = {
        'page_title': 'Home',
        'posts': Post.objects.all(),  # Example queryset, adjust as per your models
    }
    return render(request, 'topics-detail.html', context)


def topicslisting(request):
    # Replace with your logic to fetch and process data for rendering the index page
    context = {
        'page_title': 'Home',
        'posts': Post.objects.all(),  # Example queryset, adjust as per your models
    }
    return render(request, 'topics-listing.html', context)

def contact(request):
    # Replace with your logic to fetch and process data for rendering the index page
    context = {
        'page_title': 'Home',
        'posts': Post.objects.all(),  # Example queryset, adjust as per your models
    }
    return render(request, 'contact.html', context)


def update_password1(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PasswordUpdateForm(request.POST)
        if form.is_valid():
            post.password = form.cleaned_data['password']
            post.save()
            return redirect('home-page')
    else:
        form = PasswordUpdateForm()
    return render(request, 'update_password1.html', {'form': form, 'post': post})







    from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from .models import HiddenFile
from .forms import HiddenFileUploadForm, HiddenFilePasswordForm

@login_required
def upload_hidden_file(request):
    if request.method == 'POST':
        form = HiddenFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            hidden_file = form.save(commit=False)
            hidden_file.user = request.user
            hidden_file.password = make_password(form.cleaned_data['password'])  # Hash password
            hidden_file.save()
            return redirect('hidden_file_list')
    else:
        form = HiddenFileUploadForm()
    return render(request, 'upload_hidden_file.html', {'form': form})

@login_required
def access_hidden_file_list(request):
    if request.method == 'POST':
        form = HiddenFilePasswordForm(request.POST)
        if form.is_valid():
            entered_password = form.cleaned_data['password']
            # Verify password for all hidden files
            hidden_files = HiddenFile.objects.filter(user=request.user)
            for hidden_file in hidden_files:
                if check_password(entered_password, hidden_file.password):
                    return redirect('hidden_file_list')
            return render(request, 'password_protect1.html', {'error': 'Invalid password', 'form': form})
    else:
        form = HiddenFilePasswordForm()
    return render(request, 'password_protect1.html', {'form': form})

@login_required
def hidden_file_list(request):
    hidden_files = HiddenFile.objects.filter(user=request.user)
    return render(request, 'hidden_file_list.html', {'hidden_files': hidden_files})

@login_required
def access_hidden_file(request, file_id):
    hidden_file = get_object_or_404(HiddenFile, id=file_id, user=request.user)
    return render(request, 'hidden_file_detail.html', {'hidden_file': hidden_file})

from django.shortcuts import redirect, get_object_or_404
from .models import HiddenFile

def delete_hidden_file(request, file_id):
    if request.method == 'POST':
        hidden_file = get_object_or_404(HiddenFile, id=file_id)
        hidden_file.delete()
        return redirect('hidden_file_list')
    return redirect('hidden_file_list')

