from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class MetaProfesional(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_objetivo = models.DateField()

    def __str__(self):
        return f"Meta para {self.usuario.username}: {self.descripcion}"

class PlanCarrera(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    meta = models.ForeignKey(MetaProfesional, on_delete=models.CASCADE)
    descripcion = models.TextField()
    completado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plan de {self.usuario.username} para {self.meta.descripcion}"
