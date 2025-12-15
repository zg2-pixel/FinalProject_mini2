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
    selected_route = request.GET.get("route", "").strip()

    routes = (
        StopEvent.objects
        .values_list("trip__route__route_id", flat=True)
        .distinct()
        .order_by("trip__route__route_id")
    )
    routes = [r for r in routes if r]

    qs = (
        StopEvent.objects
        .select_related("stop", "trip__route")
        .values("stop__stop_id", "stop__name")
        .annotate(avg_delay=Avg("delay_seconds"))
        .order_by("-avg_delay")
    )

    if selected_route:
        qs = qs.filter(trip__route__route_id=selected_route)

    labels = [f"{r['stop__stop_id']} {r['stop__name']}" for r in qs]
    values = [float(r["avg_delay"] or 0) for r in qs]

    return render(request, "transit/dashboard.html", {
        "labels_json": json.dumps(labels),
        "values_json": json.dumps(values),
        "routes": routes,
        "selected_route": selected_route,
    })

def stop_map(request):
    route_code = request.GET.get("route")

    qs = (
        StopEvent.objects
        .select_related("stop", "trip__route")
    )

    if route_code:
        qs = qs.filter(trip__route__route_id=route_code)

    qs = (
        qs.values(
            "stop__stop_id",
            "stop__name",
            "stop__lat",
            "stop__lon",
        )
        .annotate(avg_delay=Avg("delay_seconds"))
    )

    stops = [
        {
            "id": r["stop__stop_id"],
            "name": r["stop__name"],
            "lat": float(r["stop__lat"]),
            "lon": float(r["stop__lon"]),
            "avg_delay": float(r["avg_delay"] or 0),
        }
        for r in qs
        if r["stop__lat"] is not None and r["stop__lon"] is not None
    ]

    routes = (
        StopEvent.objects
        .values_list("trip__route__route_id", flat=True)
        .distinct()
    )

    return render(
        request,
        "transit/map.html",
        {
            "stops_json": json.dumps(stops),
            "routes": routes,
            "selected_route": route_code or "",
        },
    )
