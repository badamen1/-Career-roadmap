from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Importa las vistas de autenticación

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('roadmap/<int:user_id>/', views.roadmap, name='roadmap'),
    path('editar-perfil/', views.edit_profile, name='editar_perfil'),  # Asegúrate de que 'views.edit_profile' esté aquí
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Ruta para cerrar sesión
]