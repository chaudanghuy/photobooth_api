import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Redeem
from .forms import RedeemForm
from django.views import View
from .serializers import RedeemSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages

# Create your views here.
class RedeemView(LoginRequiredMixin, ListView):
  def get(self, request):
    redeems = Redeem.objects.all().order_by('-created_at')
    return render(request, 'redeems/list.html', {"redeems": redeems})
  
class RedeemCreateView(LoginRequiredMixin, View):
  def get(self, request):
    form = RedeemForm()
    return render(request, "redeems/add.html", {"form": form})
  
  def post(self, request):
    form = RedeemForm(request.POST)
    if form.is_valid():
      code = form.cleaned_data['code']
      is_duplicated = Redeem.objects.filter(code=code).exists()
      is_active = Redeem.objects.filter(code=code, is_active=True).exists()
      
      if is_duplicated and is_active:
        messages.error(request, "Existed coupon")
        return render(request, "redeems/add.html", {"form": form})
      
      form.save()
      return redirect("redeems")
    else:
      messages.error(request, form.errors)
    return render(request, "redeems/add.html", {"form": form})

class RedeemEditView(LoginRequiredMixin, View):
  def get(self, request, pk):
    redeem = Redeem.objects.get(id=pk)
    form = RedeemForm(instance=redeem)
    return render(request, "redeems/edit.html", {"form": form, "redeem": redeem})
  
  def post(self, request, pk):
    redeem = Redeem.objects.get(id=pk)
    form = RedeemForm(request.POST, instance=redeem)
    if form.is_valid():
      code = form.cleaned_data['code']
      is_duplicated = Redeem.objects.filter(code=code).exists()      
      
      if is_duplicated and code != redeem.code:
        messages.error(request, "Existed coupon")
        return render(request, "redeems/edit.html", {"form": form, "redeem": redeem})
      
      form.save()
      return redirect("redeems")
    else:
      messages.error(request, form.errors)
    return render(request, "redeems/edit.html", {"form": form, "redeem": redeem})  
  
class RedeemDeleteView(LoginRequiredMixin, View):

  def get(self, request, pk):
    redeem = Redeem.objects.get(id=pk)
    redeem.delete()
    return redirect("redeems")  
  
class RedeemListAPI(APIView):

  def get(self, request, *args, **kwargs):
    redeems = Redeem.objects.all().order_by('-created_at')
    serializer = RedeemSerializer(redeems, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class RedeemCodeAPI(APIView):
  
  def get(self, request, code, *args, **kwargs):
    if code is None:
      return Response({'error': 'Code is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
      redeem = Redeem.objects.get(code=code)
    except Redeem.DoesNotExist:
      return Response({'error': 'Redeem not found'}, status=status.HTTP_404_NOT_FOUND)    
    serializer = RedeemSerializer(redeem)
    return Response(serializer.data, status=status.HTTP_200_OK)
