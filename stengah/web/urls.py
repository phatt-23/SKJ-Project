from django.urls import path
from .views import common as common_view
from .views import auth as auth_view
from .views import user as user_view
from .views import repo as repo_view
from .views import commit as commit_view
from .views import issue as issue_view

urlpatterns = [
    path('', common_view.index, name='index'),
    path('login/', auth_view.login_view, name='login'),
    path('register/', auth_view.register_view, name='register'),
    path('logout/', auth_view.logout_view, name='logout'),
    path('dashboard/', common_view.dashboard, name='dashboard'),
    path('u/<str:username>/', user_view.user_page, name='user_page'),
    path('u/<str:username>/r/<str:repo_name>/', repo_view.repo_page, name='repo_page'),
    path('u/<str:username>/r/', repo_view.repo_list, name='user_repo_list'),
    path('u/<str:username>/a/', user_view.upload_avatar, name='user_upload_avatar'),
    path('u/<str:username>/e/', user_view.edit_page, name='user_edit_page'),
    path('rnew/', repo_view.repo_create, name='repo_create'),
    path('search/', common_view.search_view, name='search'),
    path('u/<str:username>/r/<str:repo_name>/c/', commit_view.commit_list, name='repo_commit_list'),
    path('u/<str:username>/r/<str:repo_name>/cnew/', commit_view.commit_create, name='repo_commit_create'),
    path('u/<str:username>/r/<str:repo_name>/c/<int:commit_id>/', commit_view.commit_detail, name='repo_commit_detail'),
    path('u/<str:username>/r/<str:repo_name>/e/', repo_view.edit_page, name='repo_edit_page'),
    path('u/<str:username>/r/<str:repo_name>/i/', issue_view.repo_issue_list, name='repo_issue_list'),
    path('u/<str:username>/r/<str:repo_name>/inew/', issue_view.repo_issue_create, name='repo_issue_create'),
    path('u/<str:username>/r/<str:repo_name>/i/<int:issue_id>', issue_view.repo_issue_detail, name='repo_issue_detail'),
    path('u/<str:username>/r/<str:repo_name>/d/', repo_view.repo_delete, name='repo_delete_page'),
]
