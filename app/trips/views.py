from flask import render_template, send_from_directory
from flask.ext.login import login_required

from app.trips import trips_bp
from app.models import Trip, Route


@trips_bp.route('/<route_id>/trips/<trip_id>', methods=['GET'])
@login_required
def view(route_id, trip_id):
    trip = Trip.query.get(trip_id)
    route = Route.query.get(route_id)
    return render_template('trips/index.html', trip=trip, route=route)
