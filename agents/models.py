import uuid
from django.db import models
from django.contrib.auth.models import User

class Agent(models.Model):
    # Identificador único
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relación 1 a 1: Garantiza el límite de 1 agente por usuario
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent')
    
    # Datos de transformación
    pos_x = models.FloatField(default=0.0)
    pos_y = models.FloatField(default=0.5)
    pos_z = models.FloatField(default=0.0)
    
    # Estética
    color = models.CharField(max_length=7, default="#ffa500") # Hexadecimal
    
    # Gamificación (XP y Tipo)
    xp_level = models.IntegerField(default=1)
    
    @property
    def agent_type(self):
        """Lógica de negocio: El tipo depende del nivel de XP"""
        if self.xp_level >= 10:
            return "dog"
        return "cube"

    def __str__(self):
        return f"Agente de {self.owner.username} (Lvl {self.xp_level})"
