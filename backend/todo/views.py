from django.shortcuts import render
from rest_framework import viewsets
from .models import Todo, Category
from .serializers import TodoSerializer, CategorySerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by('-updated_at')
    serializer_class = TodoSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    