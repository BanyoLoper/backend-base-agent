import uuid
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Agent(models.Model):
    SHAPE_CHOICES = [('cube', 'Cube'), ('sphere', 'Sphere'), ('pyramid', 'Pyramid')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relación 1 a 1: Garantiza el límite de 1 agente por usuario
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent')

    xp_level = models.IntegerField(default=1)
    pos_x = models.FloatField(default=0.0)
    pos_y = models.FloatField(default=0.5)
    pos_z = models.FloatField(default=0.0)
    color = models.CharField(max_length=7, default="#ffa500") # Hexadecimal
    shape = models.CharField(max_length=20, choices=SHAPE_CHOICES, default='cube')
    
    @property
    def agent_type(self):
        """Lógica de negocio: El tipo depende del nivel de XP"""
        if self.xp_level >= 10:
            return "dog"
        return "cube"

    def __str__(self):
        return f"Agente de {self.owner.username} (Lvl {self.xp_level})"


@receiver(post_save, sender=User)
def create_user_agent(sender, instance, created, **kwargs):
    if created:
        # Creamos el agente asignado al inicio en una posición aleatoria
        Agent.objects.create(
            owner=instance, 
            pos_x=0, pos_y=0.5, pos_z=0,
            color="#3498db" # Color inicial por defecto
        )
