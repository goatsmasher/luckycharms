from django.shortcuts import render, redirect
from ..users.models import User
from .models import Event, Address
# from ..messages.models import Messages, Comments


# Create your views here.
def create(request):
    context = {
        "range" : range(1,12),
        "minutes" : ('00', 15, 30,45),
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'main_app/event_page.html', context)

def invite(request):
    return render(request, 'main_app/invite_friends.html')

def create_new(request):
    new_event = Event.objects.new_event(request.POST, request.session['user_id'])
    return redirect('main:index')

def detail(request, event_id):
    context = {
        "event_info" : Event.objects.get(id=event_id),
        "user" : User.objects.get(id=request.session['user_id']),
        # 'messages': Message.objects.filter(event=Event.objects.filter(id=event_id)),
        # 'comments': Comment.objects.filter(related_message__event=Event.objects.filter(id=event_id)),
    }
    # print context["event_info"].created_by
    # print request.session
    return render(request, 'events/event_details.html', context)