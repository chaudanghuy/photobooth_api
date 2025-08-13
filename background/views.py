import requests
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Background, Frame
from .serializers import BackgroundSerializer
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from .forms import BackgroundForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings

import cloudinary.uploader

# Create your views here.

BACKGROUND_POSITIONS = ['row-1-1', 'row-1-2', 'row-1-3', 'row-1-4', 'row-1-5']

BACKGROUND_API_URL = settings.DEV_URL + "backgrounds/api"

FRAME_API_URL = settings.DEV_URL + "frames/api"

POSITION_LIST = ['row-1-1', 'row-1-2', 'row-1-3', 'row-1-4', 'row-1-5', 'row-1-6', 'row-1-7', 'row-1-8', 'row-1-9', 'row-1-10']

class BackgroundAPI(APIView):    
    
    def get(self, request, *args, **kwargs):
        backgrounds = Background.objects.exclude(title='')
        serializer = BackgroundSerializer(backgrounds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)     
    
    def post(self, request, *args, **kwargs):
        form = BackgroundForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Background created successfully"}, status=201)
        else:
            messages.error(request, form.errors)
        return JsonResponse({"message": "Failed to create background"}, status=400)
    
class BackgroundDetailAPI(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk, *args, **kwargs):
        background = Background.objects.get(id=pk)
        serializer = BackgroundSerializer(background)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, *args, **kwargs):
        background = Background.objects.get(id=pk)
        data = request.data.copy()

        if 'photo' not in request.FILES and not data.get('photo'):
            data['photo'] = background.photo  # keep existing
        else:
            photo_file = request.FILES.get('photo')
            if photo_file:
                upload_data = cloudinary.uploader.upload(photo_file)
                data['photo'] = upload_data.get('url')

        # photo_hover
        if 'photo_hover' not in request.FILES and not data.get('photo_hover'):
            data['photo_hover'] = background.photo_hover  # keep existing
        else:
            photo_hover_file = request.FILES.get('photo_hover')
            if photo_hover_file:
                upload_data = cloudinary.uploader.upload(photo_hover_file)
                data['photo_hover'] = upload_data.get('url')

        # photo_kr
        if 'photo_kr' not in request.FILES and not data.get('photo_kr'):
            data['photo_kr'] = background.photo_kr  # keep existing
        else:
            photo_kr_file = request.FILES.get('photo_kr')
            if photo_kr_file:
                upload_data = cloudinary.uploader.upload(photo_kr_file)
                data['photo_kr'] = upload_data.get('url')
        
        # photo_kr_hover
        if 'photo_kr_hover' not in request.FILES and not data.get('photo_kr_hover'):
            data['photo_kr_hover'] = background.photo_kr_hover  # keep existing
        else:
            photo_kr_hover_file = request.FILES.get('photo_kr_hover')
            if photo_kr_hover_file:
                upload_data = cloudinary.uploader.upload(photo_kr_hover_file)
                data['photo_kr_hover'] = upload_data.get('url')
        
        # photo_vn
        if 'photo_vn' not in request.FILES and not data.get('photo_vn'):
            data['photo_vn'] = background.photo_vn  # keep existing
        else:
            photo_vn_file = request.FILES.get('photo_vn')
            if photo_vn_file:
                upload_data = cloudinary.uploader.upload(photo_vn_file)
                data['photo_vn'] = upload_data.get('url')
        
        # photo_vn_hover
        if 'photo_vn_hover' not in request.FILES and not data.get('photo_vn_hover'):
            data['photo_vn_hover'] = background.photo_vn_hover  # keep existing
        else:
            photo_vn_hover_file = request.FILES.get('photo_vn_hover')
            if photo_vn_hover_file:
                upload_data = cloudinary.uploader.upload(photo_vn_hover_file)
                data['photo_vn_hover'] = upload_data.get('url')

        form = BackgroundForm(data, instance=background)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Background updated successfully"}, status=201)
        
        return JsonResponse({"message": "Failed to update background"}, status=400)
    
    def delete(self, request, pk, *args, **kwargs):
        background = Background.objects.get(id=pk)
        background.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        

class BackgroundList(LoginRequiredMixin, ListView):
    
    def get(self, request):
        frameId = request.GET.get('frame') or 0
        frame = Frame.objects.get(id=frameId)
        backgrounds = Background.objects.all()
        frames = Frame.objects.all()
        return render(request, 'backgrounds/list.html', {'positions': BACKGROUND_POSITIONS, 'backgrounds': backgrounds, 'frames': frames, 'frame': frame, 'frameId': int(frameId), 'position_list': POSITION_LIST})
    
    def post(self, request):
        data = request.POST.copy()        

        if 'photo' in request.FILES:
            upload_data = cloudinary.uploader.upload(request.FILES['photo'])
            data['photo'] = upload_data.get('url')

        if 'photo_hover' in request.FILES:
            upload_data = cloudinary.uploader.upload(request.FILES['photo_hover'])
            data['photo_hover'] = upload_data.get('url')

        if 'photo_kr' in request.FILES:
            upload_data = cloudinary.uploader.upload(request.FILES['photo_kr'])
            data['photo_kr'] = upload_data.get('url')

        if 'photo_kr_hover' in request.FILES:
            upload_data = cloudinary.uploader.upload(request.FILES['photo_kr_hover'])
            data['photo_kr_hover'] = upload_data.get('url')

        if 'photo_vn' in request.FILES:
            upload_data = cloudinary.uploader.upload(request.FILES['photo_vn'])
            data['photo_vn'] = upload_data.get('url')

        if 'photo_vn_hover' in request.FILES:
            upload_data = cloudinary.uploader.upload(request.FILES['photo_vn_hover'])
            data['photo_vn_hover'] = upload_data.get('url')
            
        form = BackgroundForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Background created successfully"}, status=201)
        else:
            messages.error(request, form.errors)
            return JsonResponse({"message": "Failed to create background"}, status=400)
    
    def put(self, request, pk):
        background = Background.objects.get(id=pk)
        form = BackgroundForm(request.POST, request.FILES, instance=background)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Background updated successfully"}, status=201)
        else:
            messages.error(request, form.errors)
        return JsonResponse({"message": "Failed to update background"}, status=400)