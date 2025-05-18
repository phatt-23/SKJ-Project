from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.http.request import BadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.translation import trim_whitespace
from common.models import Repository


def user_page(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    repos = Repository.objects.filter(owner=user)
   
    is_my_page = username == request.user.username if request.user.is_authenticated else False

    return render(request, 'web/user_page.html', {
        'pub_user': user,
        'repos': repos,
        'is_my_page': is_my_page
    })


@login_required
def upload_avatar(request: HttpRequest, username):
    if request.user.username != username:
        raise BadRequest('You cannot upload avatar of another user.') 

    if request.method == 'POST' and request.FILES.get('avatar'):
        avatar = request.FILES['avatar']
        request.user.avatar.save(avatar.name, avatar, save=True)
        return redirect('user_page', username=request.user.username)

    return render(request, 'web/user_upload_avatar.html')


@login_required
def edit_page(request: HttpRequest, username):
    user = get_object_or_404(get_user_model(), username=request.user.username)

    if user.username != username:
        return BadRequest('Cannot edit other users.')
    
    if request.method == 'POST':
        user.email = request.POST.get('email')

        bio = trim_whitespace(str(request.POST.get('bio')))
        user.bio = bio if bio else ''  
        
        if 'remove_avatar' in request.POST:
            user.avatar.delete()
        elif 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        user.save()

        return redirect('user_page', username=user.username)

    return render(request, 'web/user_edit_page.html', {
        'pub_user': user
    })


