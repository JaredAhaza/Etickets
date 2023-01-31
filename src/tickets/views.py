from django.shortcuts import render, redirect
from django.views import View
from tickets.models import AtendeeUser, Location, TicketType, Event, Booking
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from tickets.forms import EventForm
from datetime import timezone, datetime, timedelta


# Create your views here.

# homepage view

class Home(View):
    def get(self, request):
        form = EventForm
        return render(request, 'home.html', {'form': form})

class AvailableEvent(View):
    def get(self, request):
        if request.GET:

            start_time = request.GET.get('start_time')
            end_time = request.GET.get('end_time')
            date = request.GET.get('date')
            ttype = request.GET.get('ttype')
            adult = request.GET.get('pa')
            child = request.GET.get('pc')

            adult = int(adult)
            child = int(child)

            if start_time == '' or start_time == 'Select' or end_time == '' or end_time == 'Select' \
                    or date == '' or date == 'mm//dd//yyyy' or ttype == '':
                messages.warning(request, 'Please fillup the form properly')
                return redirect('home')

            elif (adult + child) < 1:
                messages.warning(request, 'Please book minimum 1 seat')
                return redirect('home')

            elif (adult + child) > 5:
                messages.warning(request, 'You can book maximum 5 seat')
                return redirect('home')

            else:
                search = Event.objects.filter(start_time=start_time, end_time=end_time, ticket_type=ttype)
                
                start_time = Location.objects.get(pk=start_time)
                end_time = Location.objects.get(pk=end_time)
                ticket_type = TicketType.objects.get(pk=ttype)
                
                return render(request, 'available_Event.html', {'search': search, 'start_time':start_time, 'end_time':end_time, 'ticket_type':ticket_type})

        else:
            messages.warning(request, 'Find Event first to get available Event')
            return redirect('home')
