import requests
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Store
from .serializers import StoreSerializer
from .forms import StoreForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages

# Create your views here.
class StoreAPI(APIView):
    def get(self, request, *args, **kwargs):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreDetailAPI(APIView):
    def get(self, request, pk, *args, **kwargs):
        store = Store.objects.get(id=pk)
        serializer = StoreSerializer(store)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, *args, **kwargs):
        store = Store.objects.get(id=pk)
        serializer = StoreSerializer(instance=store, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        store = Store.objects.get(id=pk)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StoreListView(LoginRequiredMixin, View):    
    def get(self, request):
        stores = Store.objects.all()
        return render(request, 'stores/list.html', {'stores': stores})

class AddStoreView(LoginRequiredMixin, View):
    def get(self, request):
        form = StoreForm(initial={'created_at': timezone.now(), 'updated_at': timezone.now()})                
        return render(request, 'stores/add.html', {'form': form})

    def post(self, request):
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store added successfully!')
            return redirect('stores')
        else:
            messages.error(request, 'Add failed!')
        return render(request, 'stores/add.html', {'form': form})

class EditStoreView(LoginRequiredMixin, View):
    def get(self, request, pk):
        store = Store.objects.get(id=pk)
        store.updated_at = timezone.now()
        form = StoreForm(instance=store)
        return render(request, 'stores/edit.html', {'form': form, 'store': store})

    def post(self, request, pk):
        store = Store.objects.get(id=pk)
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('stores')
        else:
            messages.error(request, 'Edit Failed!')
        return render(request, 'stores/edit.html', {'form': form, 'store': store})
