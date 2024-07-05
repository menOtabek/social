from django.shortcuts import render, redirect
from .models import Post, MyUser, CommentPost, LikePost, FollowMyUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


@login_required(login_url='/login')
def index_view(request):
    comments = CommentPost.objects.filter(is_visible=True)

    like_post = LikePost.objects.all()
    users = MyUser.objects.exclude(user=request.user)
    my_user = MyUser.objects.filter(user=request.user).first()
    followings = FollowMyUser.objects.filter(follower=my_user).values_list('following', flat=True)
    display_users = users.exclude(id__in=followings)
    posts = Post.objects.filter(is_published=True, author__in=followings)
    if posts.count() == 0:
        posts = Post.objects.filter(is_published=True, author=my_user)

    for post in posts:
        post.like_post = like_post.filter(post_id=post.id).order_by('-created_at')[:1]
        post.comments = comments.filter(post_id=post.id)

    context = {
        'posts': posts,
        'user': MyUser.objects.filter(user=request.user).first(),
        'profiles': display_users[:4],
        'profile': MyUser.objects.filter(user=request.user),
        'my_user': my_user,
    }

    if request.method == 'POST':
        data = request.POST
        message = data['message']
        post_id = data['post_id']
        my_user = MyUser.objects.filter(user=request.user).first()
        obj = CommentPost.objects.create(message=message, post_id=post_id, author=my_user)
        obj.save()
        my_post = Post.objects.get(id=post_id)
        my_post.comment_count += 1
        my_post.save(update_fields=['comment_count'])

        return redirect('/#{}'.format(post_id))

    return render(request, 'index.html', context=context)


def login_view(request):
    context = {}
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            context['error'] = 'User with this username does not exists'
    return render(request, 'signin.html', context=context)


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/login')


def register_view(request):
    context = {}
    if request.method == 'POST':
        data = request.POST
        username = data['username'].lower()
        password1 = data['password1']
        password2 = data['password2']

        if not User.objects.filter(username=username).exists() and password1 == password2:
            user = User.objects.create(username=username, password=make_password(password1))
            user.save()
            my_user = MyUser.objects.create(user=user)
            my_user.save()
            return redirect('/login')
        context['error'] = 'User with this username already exists or passwords did not match'
    return render(request, 'signup.html', context=context)


def upload_view(request):
    if request.method == 'POST':
        my_user = MyUser.objects.filter(user=request.user).first()
        post = Post.objects.create(post_image=request.FILES['post_image'], author=my_user)
        post.save()
        return redirect('/')
    return redirect('/')


def profile_settings_view(request):
    if request.method == 'POST':
        my_user = MyUser.objects.filter(user=request.user).first()
        picture = MyUser.objects.create(profile_picture=request.FILES['profile_picture'], author=my_user)
        picture.save()
        return redirect('/')
    return render(request, 'setting.html')


def follow_view(request):
    profile_id = request.GET.get('profile_id')
    my_user = MyUser.objects.filter(user=request.user).first()
    profile = MyUser.objects.filter(id=profile_id).first()
    following = MyUser.objects.filter(id=request.user.id).first()
    follow_exists = FollowMyUser.objects.filter(follower=my_user, following_id=profile_id)

    if not follow_exists.exists():
        obj = FollowMyUser.objects.create(follower=my_user, following_id=profile_id)
        obj.save()
        profile.follower_count += 1
        profile.save(update_fields=['follower_count'])
        following.following_count += 1
        following.save(update_fields=['following_count'])

    else:
        follow_exists.delete()
        profile.follower_count -= 1
        profile.save(update_fields=['follower_count'])
        following.following_count -= 1
        following.save(update_fields=['following_count'])
    return redirect('/')


def like_view(request):
    post_id = request.GET.get('post_id')
    my_user = MyUser.objects.filter(user=request.user).first()
    my_post = Post.objects.filter(id=post_id).first()
    like_exists = LikePost.objects.filter(author=my_user, post_id=post_id)

    if not like_exists.exists():
        obj = LikePost.objects.create(author=my_user, post_id=post_id)
        obj.save()
        my_post.like_count += 1
        my_post.save(update_fields=['like_count'])

    else:
        like_exists.delete()
        my_post.like_count -= 1
        my_post.save(update_fields=['like_count'])
    return redirect('/#{}'.format(post_id))


def profile_view(request):
    user_id = request.GET.get('profile_id')
    user = MyUser.objects.filter(id=user_id).first()
    my_user = MyUser.objects.filter(user_id=request.user.id).first()
    posts = Post.objects.filter(author=user).order_by('-created_at')
    follower = FollowMyUser.objects.filter(following_id=user_id).values_list('follower', flat=True)
    following = FollowMyUser.objects.filter(follower_id=user_id).values_list('following', flat=True)
    follower_count = FollowMyUser.objects.filter(following=user).count()
    following_count = FollowMyUser.objects.filter(follower=user).count()
    context = {
        'user': user,
        'posts': posts,
        'follower_count': follower_count,
        'following_count': following_count,
        'following': following,
        'follower': follower,
        'post_count': posts.count(),
    }
    if user == my_user:
        if request.method == 'POST':
            # my_user = MyUser.objects.filter(user=request.user).first()
            user.profile_image = request.FILES['profile_image']
            user.save(update_fields=['profile_image'])
            return redirect('/profile/?profile_id={}'.format(user.id))

        return render(request, 'myprofile.html', context=context)

    return render(request, 'profile.html', context=context)


def search_view(request):
    if request.method == 'POST':
        data = request.POST
        query = data['query']
        return redirect(f'/search?q={query}')
    query = request.GET.get('q')
    posts = Post.objects.all()
    if query is not None and len(query) >= 1:
        posts = posts.filter(author__user__username__icontains=query)

    comments = CommentPost.objects.filter(is_visible=True)
    like_post = LikePost.objects.all()
    users = MyUser.objects.exclude(user=request.user)
    my_user = MyUser.objects.filter(user=request.user).first()
    followings = FollowMyUser.objects.filter(follower=my_user).values_list('following', flat=True)
    display_users = users.exclude(id__in=followings)
    context = {
        'posts': posts,
        'user': MyUser.objects.filter(user=request.user).first(),
        'profiles': display_users[:4],
        'comments': comments,
        'like_post': like_post,
        'profile': MyUser.objects.filter(user=request.user),
        'my_user': my_user,
    }
    return render(request, 'index.html', context=context)

# def post_delete_view(request):
#     post_id = request.GET.get('post_id')
#     print(post_id)
#     print('*' * 70)
#     my_user = MyUser.objects.filter(user=request.user).first()
#     post = Post.objects.filter(id=post_id).first()
#     if post.author == my_user:
#         post.delete()
#         return redirect('/')
#     return redirect('/')
