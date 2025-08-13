import requests
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Layout
from .serializers import LayoutSerializer
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from .forms import LayoutForm
from django.contrib.auth.mixins import LoginRequiredMixin
from background.models import Background
from django.core.paginator import Paginator
from frame.models import Frame
from django.conf import settings
from background.models import Background
from frame.models import Frame

import cloudinary.uploader

# Create your views here.

BACKGROUND_API_URL = settings.DEV_URL + "backgrounds/api"

FRAME_API_URL = settings.DEV_URL + "frames/api"

POSITION_LIST = ['row-1-1', 'row-1-2', 'row-1-3', 'row-1-4', 'row-1-5', 'row-1-6', 'row-1-7', 'row-1-8', 'row-1-9', 'row-1-10']


def get_background_list():
    response = requests.get(BACKGROUND_API_URL)
    if response.status_code == 200:
        return response.json()
    return []

def get_frame_list():
    response = requests.get(FRAME_API_URL)
    if response.status_code == 200:
        return response.json()
    return []

class LayoutAPI(APIView):
    
    def get(self, request, *args, **kwargs):
        layouts = Layout.objects.all()
        serializer = LayoutSerializer(layouts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()

        if 'photo' in request.FILES:
            upload_data = cloudinary.uploader.upload(request.FILES['photo'])
            data['photo'] = upload_data.get('url')

        if 'photo_cover' in request.FILES:
            upload_data = cloudinary.uploader.upload(request.FILES['photo_cover'])
            data['photo_cover'] = upload_data.get('url')

        if 'photo_full' in request.FILES:
            upload_data = cloudinary.uploader.upload(request.FILES['photo_full'])
            data['photo_full'] = upload_data.get('url')

        form = LayoutForm(data)
        
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Layout created successfully"}, status=201)                    
        return JsonResponse({"message": "Failed to create layout"}, status=400)
    
class LayoutDetailAPI(APIView):
    
        permission_classes = [permissions.IsAuthenticated]
    
        def get(self, request, pk, *args, **kwargs):
            layout = Layout.objects.get(id=pk)
            serializer = LayoutSerializer(layout)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        def put(self, request, pk, *args, **kwargs):
            layout = Layout.objects.get(id=pk)
            data = request.data.copy()

            if 'photo' not in request.FILES and not data.get('photo'):
                data['photo'] = layout.photo  # keep existing
            else: 
                photo_file = request.FILES.get('photo')
                if photo_file:
                    upload_data = cloudinary.uploader.upload(photo_file)
                    data['photo'] = upload_data.get('url')
            
            if 'photo_cover' not in request.FILES and not data.get('photo_cover'):
                data['photo_cover'] = layout.photo_cover  # keep existing
            else: 
                photo_cover_file = request.FILES.get('photo_cover')
                if photo_cover_file:
                    upload_data = cloudinary.uploader.upload(photo_cover_file)
                    data['photo_cover'] = upload_data.get('url')
            
            if 'photo_full' not in request.FILES and not data.get('photo_full'):
                data['photo_full'] = layout.photo_full  # keep existing
            else: 
                photo_full_file = request.FILES.get('photo_full')
                if photo_full_file:
                    upload_data = cloudinary.uploader.upload(photo_full_file)
                    data['photo_full'] = upload_data.get('url')

            form = LayoutForm(data, instance=layout)
            backgrounds = Background.objects.all()
            frames = Frame.objects.all()
            if form.is_valid():
                form.save()
                return JsonResponse({"message": "Layout updated successfully"}, status=201)
            return JsonResponse({"message": "Failed to update layout"}, status=400)
    
        def delete(self, request, pk, *args, **kwargs):
            layout = Layout.objects.get(id=pk)
            layout.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class LayoutByBackgroundAPI(APIView):
    def get(self, request, background, frame, *args, **kwargs):
        background = Background.objects.get(title=background)
        frame = Frame.objects.get(title=frame)
        layouts = Layout.objects.filter(background=background.id, frame=frame.id)
        serializer = LayoutSerializer(layouts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LayoutGroupByBackgroundAPI(APIView):
    def get(self, request, id, frame, *args, **kwargs):
        frame = Frame.objects.get(pk=frame)
        background = Background.objects.get(pk=id)
        if frame:
            layouts = Layout.objects.filter(background=background.id, frame=frame.id)
        else:
            layouts = Layout.objects.filter(background=background.id)        
        serializer = LayoutSerializer(layouts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class LayoutList(LoginRequiredMixin, ListView):
    def get(self, request):                
        page_number = request.GET.get('page')
        background_query = request.GET.get('background')
        
        all_data = Layout.objects.all().order_by('-id')
        if background_query:
            background = Background.objects.get(id=background_query)
            all_data = Layout.objects.filter(background=background.id).order_by('-id')        
        
        backgrounds = Background.objects.all()
        frames = Frame.objects.all()
        return render(request, 'layouts/list.html', {'layouts': all_data, 'backgrounds': backgrounds, 'frames': frames, 'position_list': POSITION_LIST})

class LayoutCreateView(LoginRequiredMixin, View):
    template_name = 'layouts/add.html'
    def get(self, request):
        form = LayoutForm()
        frames = Frame.objects.all()
        backgrounds = Background.objects.all()
        return render(request, self.template_name, {'form': form, 'backgrounds': backgrounds, 'frames': frames,  'position_list': POSITION_LIST})

    def post(self, request):
        form = LayoutForm(request.POST, request.FILES)
        backgrounds = Background.objects.all()
        frames = Frame.objects.all()
        if form.is_valid():
            form.save()
            return redirect(f'{reverse_lazy("layouts")}?background={form.instance.background.id}')
        return render(request, self.template_name, {'form': form, 'backgrounds': backgrounds, 'frames': frames, 'position_list': POSITION_LIST})

class LayoutEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        layout = Layout.objects.get(id=pk)
        backgrounds = Background.objects.all()
        frames = Frame.objects.all()
        form = LayoutForm(instance=layout)
        return render(request, 'layouts/edit.html', {'form': form, 'backgrounds': backgrounds, 'frames': frames, 'layout': layout, 'position_list': POSITION_LIST})

    def post(self, request, pk):
        layout = Layout.objects.get(id=pk)
        form = LayoutForm(request.POST, request.FILES, instance=layout)
        backgrounds = Background.objects.all()
        frames = Frame.objects.all()
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('layouts'))
        return render(request, 'layouts/edit.html', {'form': form, 'backgrounds': backgrounds, 'frames': frames, 'layout': layout, 'position_list': POSITION_LIST})
    
class LayoutDeleteView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        layout = Layout.objects.get(id=pk)
        layout.delete()
        return redirect(reverse_lazy('layouts'))    