from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserProfile
from .chatbot import chatbot
from .forms import UserProfileForm  # Asegúrate de que esta línea esté presente
from django.contrib.auth import logout
def home(request):
    return render(request, 'roadmap/index.html')

@login_required
def chat(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_input = request.POST.get('message')
        chat_history = profile.chat_history
        response = chatbot.get_response(user_input, chat_history)
        
        # Agregar el mensaje y la respuesta al historial
        chat_history.append({"user": user_input, "ai": response})
        profile.chat_history = chat_history
        profile.save()
        
        return JsonResponse({"message": response})
    
    return render(request, 'roadmap/chat.html')

@login_required
def roadmap(request, user_id):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'roadmap/roadmap.html', {'profile': profile, 'user': request.user})

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'roadmap/profile.html', {'profile': profile})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'roadmap/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'roadmap/login.html', {'form': form})
@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('Home')  # Redirige a la vista del roadmap
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'roadmap/editar_perfil.html', {'form': form})
@login_required 
def logout_view(request):
    logout(request)
    return redirect('home')
