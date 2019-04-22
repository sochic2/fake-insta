from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, ProfileForm, CustomUserCreationForm
from .models import Profile

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # 프로필도 생성
            auth_login(request, user)
            return redirect('posts:list')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/signup.html', context)
    
    
def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'posts:list')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/login.html', context)
    
def logout(request):
    auth_logout(request)
    return redirect('posts:list')
    
def people(request, username):
    people = get_object_or_404(get_user_model(), username=username)
    context = {
        'people':people,
        }
    return render(request, 'accounts/people.html', context)
 
@login_required  
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'post_form':form}
    return render(request, 'accounts/update.html', context)
    
@login_required      
def delete(request):
    if request.method == 'POST':
        request.user.delete()
    return redirect('posts:list')
    
@login_required
def password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)             # 바뀌고 로그아웃 안되게 바꾸는거...? 위에 import도 하고 이거 써주고, user 
            return redirect('people', request.user.username)    # 없으니까 user에 위의 password_change_form.save() 담고 그걸 hash 옆에 ㄱㄱ
        
    else:
        password_change_form = PasswordChangeForm(request.user) #user = request.user 인데 위치로 알수있어서 앞의 user는 생략 가능
    context = {'password_change_form': password_change_form}
    return render(request, 'accounts/password.html', context)

@login_required
def profile_update(request):
    profile = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('people', request.user.username)
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    context = {'profile_form':profile_form}
    return render(request, 'accounts/profile_update.html', context)
    
@login_required
def follow(request, user_pk):
    people = get_object_or_404(get_user_model(), pk=user_pk)
    # people이 팔로워하고 있는 모든 유저에 현재 접속 유저가 있다면, unfollow
    # 아니면 follow
    if request.user in people.followers.all():
        people.followers.remove(request.user)    
    
    else:
        people.followers.add(request.user)
    return redirect('people', people.username)