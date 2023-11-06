from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


# Create your views here.

def cinephile_register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/login?register=true')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})