from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, ProfileEditForm, UserEditForm, UserRegistrationForm, \
                   UserEditForm, ProfileEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.
# def user_login(request):
#     """a view to authenticate user against
#         database using username and password
#         retrieved from the user using LoginForm
#     """
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponse('Authenticated Successfully!')
#             else:
#                 return HttpResponse('Sorry this user is disabled')
#         else:
#             return HttpResponse('invalid login')
#     else:
#         form = LoginForm()

#     context = {'form': form,}
#     return render(request, 'account/login.html', context)

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def  register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #  Create a new user object but avoid saving it yet.
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {'new_user':new_user}
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()

    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

@login_required
def edit(request):
    """ handle user and profile edit """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully.')
        else:
            messages.error(request, 'Error Updating your profile.')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {'user_form':user_form,
               'profile_form':profile_form,}

    return render(request, 'account/edit.html', context)
