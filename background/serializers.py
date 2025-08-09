from rest_framework import serializers
from .models import Background

class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = '__all__'
        read_only_fields = ['user']