from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from common.models import Repository

def user_page(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    repos = Repository.objects.filter(owner=user, is_public=True)

    return render(request, 'web/user_page.html', {
        'pub_user': user,
        'repos': repos,
    })
