from rest_framework import serializers
from .models import EventMedia, Users,Add_event

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields='__all__'
class Add_eventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Add_event
        fields='__all__'

class EventMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMedia
        fields = ['id', 'user', 'event', 'name', 'description', 'video', 'image', 'uploaded_at']
