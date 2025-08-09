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
        form = BackgroundForm(request.POST, request.FILES, instance=background)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Background updated successfully"}, status=201)
        else:
            messages.error(request, form.errors)
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
        form = BackgroundForm(request.POST, request.FILES)
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