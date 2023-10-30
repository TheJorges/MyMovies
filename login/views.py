from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def cinephile_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/movies')
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas', 'form':AuthenticationForm()})
    return render(request, 'login.html', {'form': AuthenticationForm()})

@login_required
def cinephile_logout(request):
    logout(request)
    return redirect('/movies')
