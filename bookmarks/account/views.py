from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.
def user_login(request):
    """a view to authenticate user against
        database using username and password
        retrieved from the user using LoginForm
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Authenticated Successfully!')
            else:
                return HttpResponse('Sorry this user is disabled')
        else:
            return HttpResponse('invalid login')
    else:
        form = LoginForm()

    context = {'form': form,}
    return render(request, 'account/login.html', context)