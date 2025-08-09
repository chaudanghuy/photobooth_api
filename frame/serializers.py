from rest_framework import serializers
from .models import Frame, CloudPhoto

class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = '__all__'

    def get_photo(self, obj):
        return self._build_photo_url(obj.photo)

    def get_photo_hover(self, obj):
        return self._build_photo_url(obj.photo_hover)

    def _build_photo_url(self, field_value):
        """
        If it's already a full URL (starts with http/https),
        return as is; otherwise build full absolute URI.
        """
        if not field_value:
            return None
        field_str = str(field_value)
        if field_str.startswith("http://") or field_str.startswith("https://"):
            return field_str
        request = self.context.get("request")
        return request.build_absolute_uri(field_value.url if hasattr(field_value, "url") else field_value)
        
class CloudPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudPhoto
        fields = '__all__'        