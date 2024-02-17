from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serialzers import UserSerialzer
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerialzer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def login(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        password = request.POST.get('password')
        user = authenticate(request, id=id, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message':'login success'})
        else:
            return JsonResponse({'message':'login fail'}, status=400)
# Create your views here.
