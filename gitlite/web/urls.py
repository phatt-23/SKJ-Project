from django.urls import path
from .views import common as common_view
from .views import auth as auth_view
from .views import user as user_view
from .views import repo as repo_view

urlpatterns = [
    path('', common_view.index, name='index'),
    path('login/', auth_view.login_view, name='login'),
    path('register/', auth_view.register_view, name='register'),
    path('logout/', auth_view.logout_view, name='logout'),
    path('dashboard/', common_view.dashboard, name='dashboard'),
    path('u/<str:username>/', user_view.user_page, name='user_page'),
    path('u/<str:username>/r/<str:repo_name>/', repo_view.repo_page, name='repo_page'),
    path('u/<str:username>/r/', repo_view.repo_list, name='user_repo_list'),
    path('repo/create/', repo_view.repo_create, name='repo_create'),
    path('search/', common_view.search_view, name='search'),
    path('u/<str:username>/a/', user_view.upload_avatar, name='user_upload_avatar')
]
