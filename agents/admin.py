from django.contrib import admin
from .models import Agent

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'xp_level', 'agent_type', 'color')
    list_filter = ('xp_level',)
    readonly_fields = ('id',)
