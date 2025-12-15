import json
from django.db.models import Avg
from django.shortcuts import render, redirect
from .models import StopEvent
from .forms import StopEventForm


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

def dashboard(request):
    qs = (
        StopEvent.objects
        .select_related("stop")
        .values("stop__stop_id", "stop__name")
        .annotate(avg_delay=Avg("delay_seconds"))
        .order_by("-avg_delay")
    )

    labels = [f"{r['stop__stop_id']} {r['stop__name']}" for r in qs]
    values = [float(r["avg_delay"] or 0) for r in qs]

    return render(request, "transit/dashboard.html", {
        "labels_json": json.dumps(labels),
        "values_json": json.dumps(values),
    })
