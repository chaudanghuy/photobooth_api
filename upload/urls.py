from django.urls import path
from .views import upload_file

urlpatterns = [
    path('', upload_file, name='upload_file'),  # upload 앱의 루트 URL로 설정

]
