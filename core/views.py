from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('room', room_name='default_room')  # Change 'default_room' as needed
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')

@login_required
def room(request, room_name):
    context = {"room_name": room_name}
    return render(request, 'core/room.html', context)