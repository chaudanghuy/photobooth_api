import requests
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Device
from .serializers import DeviceSerializer
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from .forms import DeviceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from frame.models import Frame
from background.models import Background
from django.contrib import messages
from django.conf import settings
from store.models import Store

STORE_API_URL = settings.DEV_URL + 'stores/api'

def get_store_list():
    response = requests.get(STORE_API_URL)
    if response.status_code == 200:
        return response.json()
    return []

# Create your views here.
class DeviceAPI(APIView):
    def get(self, request, *args, **kwargs):
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)     
    
    def post(self, request, *args, **kwargs):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeviceDetailAPI(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk, *args, **kwargs):
        device = Device.objects.get(id=pk)
        serializer = DeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, *args, **kwargs):
        device = Device.objects.get(id=pk)
        serializer = DeviceSerializer(instance=device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        device = Device.objects.get(id=pk)
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeviceList(LoginRequiredMixin, ListView):    
    def get(self, request):
        background_query = request.GET.get('background')
        stores = Store.objects.all()
        if background_query:
            background = Background.objects.filter(id=background_query).first()
            devices = Device.objects.filter(background=background.id).order_by('-id')
        else:
            devices = Device.objects.all()        
        return render(request, 'devices/list.html', {'stores': stores, 'devices': devices})

class DeviceCreateView(View):
    def get(self, request):
        form = DeviceForm()
        stores = Store.objects.all()
        return render(request, 'devices/add.html', {'form': form, 'stores': stores})
    
    def post(self, request):
        stores = Store.objects.all()                
        form = DeviceForm(request.POST)
        form.instance.user = request.user        
        if form.is_valid():
            form.save()
            return redirect('devices')
        else:
            messages.error(request, 'Add failed!')
        return render(request, 'devices/add.html', {'form': form, 'stores': stores})    
    
class DeviceEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        stores = Store.objects.all()
        device = Device.objects.get(id=pk)
        form = DeviceForm(instance=device)
        return render(request, 'devices/edit.html', {'form': form, 'device': device, 'stores': stores})
    
    def post(self, request, pk):
        stores = Store.objects.all()
        device = Device.objects.get(id=pk)              
        form = DeviceForm(request.POST, instance=device)        
        if form.is_valid():
            form.save()
            return redirect('devices')
        return render(request, 'devices/edit.html', {'form': form, 'device': device, 'stores': stores})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs