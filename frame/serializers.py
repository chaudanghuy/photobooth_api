from rest_framework import serializers
from .models import Frame, CloudPhoto

class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = '__all__'
        
class CloudPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudPhoto
        fields = '__all__'        