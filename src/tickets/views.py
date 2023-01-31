from re import A
from django.shortcuts import render, redirect
from django.views import View
from tickets.models import AtendeeUser, Location, TicketType, Event, Booking, BookingDetail, Payment, Ticket, BillingInfo
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


class Bookings(View):
    def get(self, request):
        if request.GET:

            user = request.user
            if user.is_authenticated:
                
                Event = request.GET.get('Event')
                location = request.GET.get('location')
                place = request.GET.get('place')
                date = request.GET.get('date')
                start_time = request.GET.get('start_time')
                end_time = request.GET.get('end_time')
                ta = request.GET.get('t')
                aa = request.GET.get('aa')
                ac = request.GET.get('ac')
                ttype = request.GET.get('ttype')
                total_price = request.GET.get('total_price')

                price_each = TicketType.objects.get(name=ttype)

                # this is for booking seat according to train seat capacity

                ticket = Ticket.objects.filter(event_name=Event, event_date=date)
                # if ticket.count() < 30:
                #     print(ticket.count())
                available_seat = 30 - ticket.count()
                print(available_seat)
                ta = int(ta)
                if available_seat >= ta:

                    return render(request, 'booking.html', {'Event':Event, 'location':location, 'place':place, 'date':date, 'start_time':start_time, 'end_time':end_time, 'ta':ta, 'aa':aa, 'ac':ac, 'ttype':ttype, 'total_price':total_price, 'price_each':price_each})
                else:
                    messages.warning(request, f"sorry! {available_seat} seat is not available for this Event. Try again!")
                    return redirect('home')
            else:
                messages.warning(request, "login first to book Event")
                return redirect('login')
        else:
            messages.warning(request, 'find an event first!')
            return redirect('home')

    def post(self, request):
        user = request.user

        event = request.POST['event']
        location = request.POST['location']
        place = request.POST['place']
        event_date = request.POST['event_date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        noa = request.POST['noa']
        adult = request.POST['aa']
        child = request.POST['ac']
        ticket_type = request.POST['ttype']
        ppa = request.POST['ppa']
        total_price = request.POST['total_price']

        email = request.POST['email']
        phone = request.POST['phone']

        pay_method = request.POST['ptype']
        pay_phone = request.POST['pay_phone']
        trxid = request.POST['trxid']

        # time = Train.objects.get(departure_time=travel_time)
        # travel_time = int(travel_time)
        # time = datetime.strftime(time, "HH:MM[:ss[.uuuuuu]][TZ]")

        # logic for travel_time to store in proper format
        if start_time == 'midnight':
            start_time = '0 a.m.'
            time = start_time.split()
            x = time[0]
            y = time[1]
            x = int(x)
            if not y == 'a.m.':
                x = x + 12
            start_time = timedelta(hours = x)

        elif start_time == 'noon':
            start_time = '12 p.m.'
            time = start_time.split()
            x = time[0]
            y = time[1]
            x = int(x)
            start_time = timedelta(hours = x)

        else:
            time = start_time.split()
            x = time[0]
            y = time[1]
            x = int(x)
            if not y == 'a.m.':
                x = x + 12
            start_time = timedelta(hours = x)        

        
        booking = Booking(user=user, travel_dt=str(event_date)+ ' ' + str(start_time), event_date=event_date)

        booking_detail = BookingDetail(booking=booking, Event=Event, location=location, place=place, event_date=event_date, noa=noa, adult=adult, child=child, ticket_type=ticket_type, ppa=ppa, total_price=total_price, start_time=str(start_time), end_time=str(end_time), start_dt=str(event_date)+ ' ' + str(start_time))
        
        billing_info = BillingInfo(booking=booking, user=user, email=email, phone=phone)
        
        payment = Payment(booking=booking, user=user, pay_amount=total_price, pay_method=pay_method, phone=pay_phone, trxid=trxid)
        
        booking.save()
        booking_detail.save()
        billing_info.save()
        payment.save()

        # logic to generate ticket
        noa = int(noa)
        i = 1
        while i <= noa:
            ticket = Ticket(booking=booking, user=user, phone=phone, location=location, place=place, start_time=str(start_time), event_date=event_date, event_name=event, ticket_type=ticket_type, price=ppa)
            ticket.save()
            i+=1
        # ticket generate logic end
            
        messages.success(request, 'Congratulation! Your booking is successfull')
        return redirect('booking_history')
