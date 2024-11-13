from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Importa las vistas de autenticación
from .views import save_progress  # Asegúrate de importar la vista

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('roadmap/<int:user_id>/', views.roadmap, name='roadmap'),
    path('crear-roadmap/', views.roadmapGenerator, name='crear_roadmap'),  # Nueva ruta para crear un roadmap
    path('editar-perfil/', views.edit_profile, name='editar_perfil'),  # Asegúrate de que 'views.edit_profile' esté aquí
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Ruta para cerrar sesión
    path('signup/', views.signup, name='signup'),  # Ruta para registro
    path('login/', views.login_view, name='login'),  # Ruta para inicio de sesión
    path('displayRoadmap/<int:roadmapId>', views.displayRoadmap, name='displayRoadmap'),
    path('user/profile/', views.profile, name='user_profile'),  # Nueva ruta para el perfil del usuario
    path('save-progress/', save_progress, name='save_progress'),  # Nueva ruta para guardar progreso

]