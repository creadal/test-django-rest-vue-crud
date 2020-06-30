from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.decorators import api_view
import datetime
from django.core.mail import send_mail
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler



def send_email_notification(email_address):
    send_mail("Событие!", "Не забудьте о том, что через час у вас запланировано событие!", settings.EMAIL_HOST_USER, [email_address])


scheduler = BackgroundScheduler() 
scheduler.start()
    

@api_view(['GET', 'POST', 'DELETE'])
def event_list(request):
    if request.method == 'POST':
        event_data = JSONParser().parse(request)
        event_serializer = EventSerializer(data=event_data)

        d = datetime.datetime(*[int(i) for i in event_data["date"].replace('T', ' ').replace('-', ' ').replace(':', ' ').split()])
        scheduler.add_job(send_email_notification, 'date', run_date=d-datetime.timedelta(hours=1), args=[event_data["email"]])
        #d-datetime.timedelta(hours=1)

        if event_serializer.is_valid():
            event_serializer.save()
            return JsonResponse(event_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #send_email_notification.apply_async((event_data["email"]), countdown=event_data["date"]-datetime.timedelta(hours=1))
        
    elif request.method == 'GET':
        events = Event.objects.all().order_by('-date')
        
        title = request.GET.get('title', None)
        if title is not None:
            events = events.filter(title__icontains=title)

        filterdate = request.GET.get('filterdate', None)
        
        
        if filterdate is not None:
            if filterdate == 'day':
                print(1)
                filterdate = datetime.datetime.today() - datetime.timedelta(days=1)
            elif filterdate == 'week':
                print(2)
                filterdate = datetime.datetime.today() - datetime.timedelta(days=7)
            elif filterdate == 'month':
                print(3)
                filterdate = datetime.datetime.today() - datetime.timedelta(days=30)
            else:
                filterdate = datetime.datetime(1970, 1, 1)

            print(filterdate)
            events = events.filter(date__gte=filterdate)
            
        
        events_serializer = EventSerializer(events, many=True)
        return JsonResponse(events_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'DELETE':
        count = Event.objects.all().delete()
        return JsonResponse({'message': '{} Events were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, pk):
    # find event by pk (id)
    try: 
        event = Event.objects.get(pk=pk) 
    except Event.DoesNotExist: 
        return JsonResponse({'message': 'The event does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        event_serializer = EventSerializer(event) 
        return JsonResponse(event_serializer.data)

    elif request.method == 'PUT': 
        event_data = JSONParser().parse(request) 
        event_serializer = EventSerializer(event, data=event_data) 
        if event_serializer.is_valid(): 
            event_serializer.save() 
            return JsonResponse(event_serializer.data) 
        return JsonResponse(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE': 
        event.delete() 
        return JsonResponse({'message': 'Event was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

