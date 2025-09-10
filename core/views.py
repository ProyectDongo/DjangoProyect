# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm

def inicio(request):
    return render(request, 'core/welcome.html')



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.role == 'ENTRENADOR':
                return redirect('trainer_dashboard')
            elif user.role == 'CLIENTE':
                return redirect('client_dashboard')
            elif user.role == 'NUTRICIONISTA':
                return redirect('nutritionist_dashboard')  
            else:
                return redirect('inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})
