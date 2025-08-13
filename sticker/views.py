import requests
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Sticker
from .serializers import StickerSerializer
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpRequest, HttpResponse, JsonResponse
from .forms import StickerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

import cloudinary.uploader

# Create your views here.
class StickerAPI(APIView):
    def get(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category is not None:
            stickers = Sticker.objects.filter(category=category)
        else:
            stickers = Sticker.objects.all()
        serializer = StickerSerializer(stickers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)     
    
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()

        if 'photo' in request.FILES:
            upload_data = cloudinary.uploader.upload(request.FILES['photo'])
            data['photo'] = upload_data.get('url')
            
        form = StickerForm(data)        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            messages.error(request, form.errors)
        return JsonResponse({'success': False})
      
class StickerDetailAPI(APIView):
    
    def get(self, request, pk, *args, **kwargs):
        sticker = Sticker.objects.get(id=pk)
        serializer = StickerSerializer(sticker)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, *args, **kwargs):
        sticker = Sticker.objects.get(id=pk)        
        data = request.data.copy()

        if 'photo' not in request.FILES and not data.get('photo'):
            data['photo'] = sticker.photo  # keep existing
        else: 
            photo_file = request.FILES.get('photo')
            if photo_file:
                upload_data = cloudinary.uploader.upload(photo_file)
                data['photo'] = upload_data.get('url')

        form = StickerForm(data, instance=sticker)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            messages.error(request, form.errors)
        return JsonResponse({'error': messages})
    
    def delete(self, request, pk, *args, **kwargs):
        sticker = Sticker.objects.get(id=pk)
        sticker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)      
      
class StickerList(LoginRequiredMixin, ListView):
    model = Sticker
    template_name = 'stickers/list.html'
    context_object_name = 'stickers'      
    
class StickerCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = StickerForm()
        return render(request, 'stickers/add.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = StickerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('stickers')
        else:
            messages.error(request, form.errors)
        return render(request, 'stickers/add.html', {'form': form})
      
class StickerEditView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        sticker = Sticker.objects.get(id=pk)
        form = StickerForm(instance=sticker)
        return render(request, 'stickers/edit.html', {'form': form, 'sticker': sticker})
    
    def post(self, request, pk, *args, **kwargs):
        sticker = Sticker.objects.get(id=pk)
        form = StickerForm(request.POST, request.FILES, instance=sticker)
        if form.is_valid():
            form.save()
            return redirect('stickers')
        return render(request, 'stickers/edit.html', {'form': form, 'sticker': sticker})
    
class StickerDeleteView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        sticker = Sticker.objects.get(id=pk)
        sticker.delete()
        return redirect('stickers')    