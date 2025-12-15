from django.shortcuts import render, redirect
from .forms import StopEventForm
from .models import StopEvent

def home(request):
    return redirect("create_stop_event")

def create_stop_event(request):
    if request.method == "POST":
        form = StopEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("event_list")
    else:
        form = StopEventForm()
    return render(request, "transit/create_stop_event.html", {"form": form})

def event_list(request):
    events = StopEvent.objects.select_related("trip", "stop", "trip__route").order_by("-arrival_time")[:50]
    return render(request, "transit/event_list.html", {"events": events})
