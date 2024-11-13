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
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
from .chatbot import chatbot
from .forms import * # Asegúrate de que esta línea esté presente
from django.contrib.auth import logout,login,authenticate
import numpy as np
import json
from django.views.decorators.csrf import csrf_exempt

def __infoUser__(user):
        person = UserProfile.objects.get(user=user)
        roadmaps = list(Roadmap.objects.filter(user=person))
        context = {
            'name': user.first_name + ' ' + user.last_name,
            'username': user.username,
            'roadmaps': roadmaps,
            'city': user.city,
            'isCompany': False,
        }

        return context
@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'roadmap/userProfile.html', {'profile': profile})

def __updateCheckpointStatus(checkpoint, roadmap):
    chkpt = Checkpoint.objects.get(numberOfCheckpoint=checkpoint, roadmap=roadmap)
    chkpt.completed = not chkpt.completed  # Cambia el estado
    chkpt.save()
def __getCheckpointsStatus(roadmapId):
    query = Checkpoint.objects.filter(roadmap=roadmapId).values('numberOfCheckpoint', 'completed')
    checkpoints = {}
    for checkpoint in query:
        checkpoints[checkpoint['numberOfCheckpoint']] = checkpoint['completed']

    return checkpoints
@login_required
def checkpointUpdate(request):
    if request.method == 'POST':
        roadmapId = int(request.POST.get('roadmapId'))
        checkpoint = int(request.POST.get('checkpoint'))
        stepNumber = int(request.POST.get('stepNumber'))
        
        __updateCheckpointStatus(checkpoint, roadmapId)  # Actualiza el estado del checkpoint
        
        # Actualiza el porcentaje de finalización
        percentageCompletion(roadmapId)  # Asegúrate de llamar a esta función
        
        return redirect(f'displayRoadmap/{roadmapId}/{stepNumber}')
@login_required
def interestForm(request):
    user = User.objects.get(username=request.user)
    return render(request, 'interestForm.html', {'intereses': Intereses.objects.all()})

def createDBRoadmap(roadmapJSON, interest, person, objective, embedding):
    mainGoal = objective
    content = roadmapJSON
    completionPercentage = 0
    interest = Intereses.objects.get(name=interest) 
    numberOfLikes = 0
    roadmap = Roadmap(mainGoal=mainGoal, content=content, completionPercentage=completionPercentage, interest=interest,user=person, embedding=embedding)
    roadmap.save()
    return roadmap
def createDBCheckpoints(roadmapJSON, roadmap):
    steps = roadmapJSON['steps']
    counter = 1
    for step in steps:
        checkpoints = step['remarkablePoints']
        for _ in checkpoints:
            checkpoint = Checkpoint(numberOfCheckpoint=counter, roadmap=roadmap, completed=False)
            checkpoint.save()
            counter += 1

@login_required
def roadmapGenerator(request):
    if request.method == 'POST':
        form = RoadmapCharacteristics(request.POST)
        if form.is_valid():
            interest = form.cleaned_data['interest']
            objective = form.cleaned_data['objective']
            salary = form.cleaned_data['salary']  # Obtén el salario del formulario
            openAI = chatbot()
            roadmap = openAI.generateRoadmap(objective=objective, salary=salary)
            embedding = np.array(openAI.embedObjective(objective)).tobytes()
            
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            roadmapInstance = createDBRoadmap(roadmap, interest.name, profile, objective, embedding)
            createDBCheckpoints(roadmap, roadmapInstance)
            return redirect(f'/roadmap/displayRoadmap/{roadmapInstance.id}')
        else:
            return render(request, 'roadmap/interestForm.html', {'intereses': Intereses.objects.all(), "error": "Por favor, selecciona un interés y escribe un objetivo."})
    else:
        return render(request, 'roadmap/interestForm.html', {'intereses': Intereses.objects.all()})

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
    return render(request, 'roadmap/userProfile.html', {'profile': profile})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
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
            return redirect('home')  # Redirige a la vista del roadmap
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'roadmap/editar_perfil.html', {'form': form})
@login_required 
def logout_view(request):
    logout(request)
    return redirect('home')
def percentageCompletion(roadmapId):
    checkpoints = Checkpoint.objects.filter(roadmap=roadmapId, completed=True)
    completedCheckpoints = len(checkpoints)
    totalCheckpoints = Checkpoint.objects.filter(roadmap=roadmapId).count()

    if totalCheckpoints > 0:
        percentage = int((completedCheckpoints / totalCheckpoints) * 100)
    else:
        percentage = 0

    Roadmap.objects.filter(id=roadmapId).update(completionPercentage=percentage)
    return percentage
@login_required   
def displayRoadmap(request, roadmapId):
    try:
        roadmap = Roadmap.objects.get(id=roadmapId)
        completionPercentage = percentageCompletion(roadmapId)
        checkpoints = __getCheckpointsStatus(roadmapId)

        context = {
            'roadmap': roadmap,
            'completionPercentage': completionPercentage,
            'checkpoints': json.dumps(checkpoints),
        }
        return render(request, 'roadmap/roadmap.html', context)
    except Roadmap.DoesNotExist:
        return render(request, '404.html')  # Manejo de error si no se encuentra el roadmap

@csrf_exempt  # Solo si no estás usando CSRF en esta vista
@login_required
def save_progress(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        roadmap_id = data['roadmapId']
        checkpoints = data['checkpoints']

        for checkpoint in checkpoints:
            # Actualiza el estado de cada checkpoint
            Checkpoint.objects.filter(numberOfCheckpoint=checkpoint['number'], roadmap=roadmap_id).update(completed=checkpoint['completed'])

        # Actualiza el porcentaje de finalización
        percentageCompletion(roadmap_id)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

