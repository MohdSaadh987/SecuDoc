from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"), name="redirect-admin"),
    path('login/', auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name='login'),
    path('userlogin', views.login_user, name="login-user"),
    path('user-register', views.registerUser, name="register-user"),
    path('logout', views.logoutuser, name='logout'),
    path('profile', views.profile, name='profile'),
    path('update-profile', views.update_profile, name='update-profile'),
    # path('update-avatar', views.update_avatar, name='update-avatar'),
    path('update-password', views.update_password, name='update-password'),
    path('home-page', views.home, name='home-page'),
    path('my_posts', views.posts_mgt, name='posts-page'),
    path('manage_post', views.manage_post, name='manage-post'),
    path('manage_post/<int:pk>', views.manage_post, name='manage-post'),
    path('save_post', views.save_post, name='save-post'),
    path('delete_post', views.delete_post, name='delete-post'),
    path('shareF/<str:id>', views.shareF, name='share-file-id'),
    path('shareF/', views.shareF, name='share-file'),
    path('topics-detail/', views.topicsdetail, name='topics-detail'),
    path('topics-listing/', views.topicslisting, name='topics-listing'),
    path('contact/', views.contact, name='contact'),
    path('', views.index, name='index'),  # Index view as the homepage
      path('update-password1/<int:post_id>/', views.update_password, name='update_password'),


       path('upload-hidden-file/', views.upload_hidden_file, name='upload_hidden_file'),
    path('access-hidden-file-list/', views.access_hidden_file_list, name='access_hidden_file_list'),
    path('hidden-files/', views.hidden_file_list, name='hidden_file_list'),
    path('access-hidden-file/<int:file_id>/', views.access_hidden_file, name='access_hidden_file'),
    path('delete-hidden-file/<int:file_id>/', views.delete_hidden_file, name='delete_hidden_file'),
]
