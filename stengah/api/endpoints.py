from ninja import Router, NinjaAPI
from ninja.security import django_auth
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from common.models import Comment, Issue, Repository, Commit, File
from api.models import CommentSchema, CommitSchema, CreateCommentSchema, CreateIssueSchema, IssueSchema, RepositorySchema
from web.views.auth import User


api = NinjaAPI(auth=django_auth)


# --- Repositories ---


@api.get('/u/{username}/r/', response=list[RepositorySchema])
def list_user_repos(request, username: str):
    user = get_object_or_404(User, username=username)
    repos = Repository.objects.filter(owner=user)
    return [RepositorySchema.from_model(r) for r in repos]
    # return [{
    #     'id': r.id,
    #     'name': r.name,
    #     'owner': r.owner.username,
    # } for r in repos]


@api.get('/u/{username}/r/{repo_name}/', response=RepositorySchema)
def get_repo(request, username: str, repo_name: str):
    user = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=user, name=repo_name)
    return RepositorySchema.from_model(repo)


# --- Commits ---


@api.get('/u/{username}/r/{repo_name}/c/', response=list[CommitSchema])
def list_commits(request, username: str, repo_name: str):
    user = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=user, name=repo_name)
    commits = Commit.objects.filter(repository=repo).order_by('-timestamp')
    return [CommitSchema.from_model(c) for c in commits]


@api.get('/u/{username}/r/{repo_name}/c/{commit_id}/', response=CommitSchema)
def list_commit(request, username: str, repo_name: str, commit_id: int):
    user = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=user, name=repo_name)
    commit = Commit.objects.get(pk=commit_id)
    return CommitSchema.from_model(commit)


@api.post('u/{username}/r/{repo_name}/cnew', response=CommitSchema)
def create_commit(request, username: str, repo_name: str):
    if request.auth.username != username:
        raise HttpError(403, 'Cannot upload commit to repository not belonging to you')

    repo = get_object_or_404(Repository, name=repo_name, owner__username=username)
    message = request.POST.get('message')
    file_paths = request.POST.getlist('paths')
    uploaded_files = request.FILES.getlist('files')

    if len(file_paths) != len(uploaded_files):
        raise HttpError(400, 'File paths length doesnt match uploaded file length')

    if len(uploaded_files) == 0:
        raise HttpError(400, 'Must upload at least one file')

    commit = Commit.objects.create(repository=repo, message=message, author=request.auth)

    for p, f in zip(file_paths, uploaded_files):
        try:
            content = f.read().decode('utf-8')
        except UnicodeDecodeError:
            content = '[Could not decode file as UTF-8]'

        File.objects.create(commit=commit, path=p, content=content)

    return CommitSchema.from_model(commit)


# --- Issues ---

@api.get('/u/{username}/r/{repo_name}/i/', response=list[IssueSchema])
def list_issues(request, username: str, repo_name: str):
    user = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=user, name=repo_name)
    issues = Issue.objects.filter(repository=repo)
    return [IssueSchema.from_model(i) for i in issues]

@api.post('/u/{username}/r/{repo_name}/i/', response=IssueSchema)
def create_issue(request, username: str, repo_name: str, data: CreateIssueSchema):
    user = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=user, name=repo_name)
    issue = Issue.objects.create(repository=repo, created_by=request.user, **data.dict())
    return IssueSchema.from_model(issue)


# --- Comments ---

@api.get('/u/{username}/r/{repo_name}/i/{issue_id}/', response=list[CommentSchema])
def list_comments(request, username, repo_name, issue_id: int):
    issue = get_object_or_404(Issue, id=issue_id)
    comments = Comment.objects.filter(issue=issue)
    return [CommentSchema.from_model(c) for c in comments]

@api.get('/u/{username}/r/{repo_name}/i/{issue_id}/', response=CommentSchema)
def create_comment(request, username, repo_name, issue_id: int, data: CreateCommentSchema):
    issue = get_object_or_404(Issue, id=issue_id)
    comment = Comment.objects.create(issue=issue, author=request.user, content=data.content)
    return CommentSchema.from_model(comment)


# --- Users --- (restricted)

@api.get('/u/', response=list[str])
def list_users(request):
    return list(User.objects.values_list('username', flat=True))

@api.get('/u/{username}/', response=dict)
def get_user_info(request, username: str):
    user = get_object_or_404(User, username=username)
    return {
        'username': user.username,
    }




