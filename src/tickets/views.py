from django.shortcuts import render, redirect
from django.views import View
from app.models import AtendeeUser
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from app.forms import TrainForm
from datetime import timezone, datetime, timedelta


# Create your views here.

# homepage view

class Home(View):
    def get(self, request):
        form = EventForm
        return render(request, 'home.html', {'form': form})