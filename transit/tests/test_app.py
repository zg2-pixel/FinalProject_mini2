import pytest
from django.urls import reverse
from django.utils import timezone
from transit.models import Route, Trip, BusStop, StopEvent


@pytest.fixture
def sample_data(db):
    route = Route.objects.create(route_id="61A", name="61A – North Braddock")
    stop = BusStop.objects.create(stop_id="ST01", name="CMU Main Gate", lat=40.4433, lon=-79.9436)
    trip = Trip.objects.create(route=route, service_date=timezone.now().date())
    StopEvent.objects.create(
        trip=trip,
        stop=stop,
        arrival_time=timezone.now(),
        departure_time=timezone.now(),
        delay_seconds=45,
    )
    return {"route": route, "stop": stop, "trip": trip}


@pytest.mark.django_db
def test_pages_ok(client, sample_data):
    urls = [
        reverse("create_stop_event"),
        reverse("event_list"),
        reverse("dashboard"),
        reverse("stop_map"),
    ]
    for u in urls:
        r = client.get(u)
        assert r.status_code == 200


@pytest.mark.django_db
def test_create_stop_event_post_redirect(client, sample_data):
    trip = sample_data["trip"]
    stop = sample_data["stop"]

    payload = {
        "trip": trip.id,
        "stop": stop.id,
        "arrival_time": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
        "departure_time": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
        "delay_seconds": 12,
    }

    r = client.post(reverse("create_stop_event"), data=payload)
    assert r.status_code in (302, 303)
    assert StopEvent.objects.count() >= 2

@pytest.mark.django_db
def test_export_xlsx(client, sample_data):
    r = client.get(reverse("export_xlsx"))
    assert r.status_code == 200
    assert r["Content-Type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert r.content[:2] == b"PK"
