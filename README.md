# Transit Delay Analysis Web Application

## Overview
This is a Django web application for collecting, visualizing, and exporting public transit stop delay data.

The application includes:
- A form-based data submission view
- A dashboard with data visualization
- An interactive map view
- An Excel data export utility
- A Django admin interface
- Automated tests
- Docker containerization
- GitHub Actions CI workflow

---

## URLs

/events/new/  
Create a new stop event using a Django form.

/events/  
View all stop events.

/dashboard/  
View average delay per stop using a Chart.js bar chart.

/map/  
View bus stops and delay information on a Leaflet map.

/export/xlsx/  
Export all stop event data to an Excel (.xlsx) file.

/admin/  
Django admin interface.

---

## Data Models

Route  
- route_id  
- name  

Trip  
- route (ForeignKey to Route)  
- service_date  

BusStop  
- stop_id  
- name  
- lat  
- lon  

StopEvent  
- trip (ForeignKey to Trip)  
- stop (ForeignKey to BusStop)  
- arrival_time  
- departure_time  
- delay_seconds  

---

## Entity Relationship Diagram (ERD)

The following ERD illustrates the database schema and relationships between the core entities in this application.

- A **Route** can have multiple **Trips**
- A **Trip** belongs to one **Route** and can have multiple **StopEvents**
- A **BusStop** can appear in multiple **StopEvents**
- Each **StopEvent** links a **Trip** and a **BusStop**, recording timing and delay information

![ERD](docs/ERD.png)

---

## Excel Export

The Excel export includes the following columns:

- route_id  
- route_name  
- trip_id  
- service_date  
- stop_id  
- stop_name  
- stop_lat  
- stop_lon  
- arrival_time  
- departure_time  
- delay_seconds  

The export is implemented using openpyxl.

---

## Docker

Build the Docker image:

docker build -t transit-app .

Run the container:

docker run --rm -p 8000:8000 transit-app

The application will be available at:

http://127.0.0.1:8000/

---

## Testing

Tests are implemented using pytest and pytest-django.

Test files are located in:

transit/tests/

Run tests locally:

pytest

---

## Continuous Integration

A GitHub Actions workflow is included.

On each push:
- The Docker image is built
- All tests are executed

Workflow file:

.github/workflows/ci.yml

---

## Requirements

See requirements.txt for Python dependencies.
