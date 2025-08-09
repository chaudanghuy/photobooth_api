from django.urls import path
from .views import get_photos, serve_photo, serve_script, delete_photo

urlpatterns = [
    path('', get_photos, name='get_photo'),  # upload 앱의 루트 URL로 설정
    path('delete/<str:folder_id>/<str:image>', delete_photo, name='delete_photo'),
#path('script.js', serve_script, name='serve_script'),
    ]
