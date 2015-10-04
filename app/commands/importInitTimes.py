
# legacy
@manager.command
def importInitTimes(filename, grupo):
  """Creates stop names from other columns
    grupo is one of 01, 02, 03, ...
  """
  import csv

  codes = {}
  with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      print row
      card_code = row["codigo"]
      row["service_id"] = row["service_id"].lower()
      row["trip_start_time"] = row["trip_start_time"] + ":00"
      codes.setdefault(card_code, [])
      codes[card_code].append(row)

  startTimeRows = []

  for card_code, times in codes.items():
    print "\n", card_code
    trips = Trip.query.order_by(Trip.route_id).\
      filter(Trip.route_id.ilike(grupo + '%'), Trip.card_code == card_code).all()
    for trip in trips:
      for time in times:
        tripStartTime = TripStartTime(service_id=time["service_id"],
          start_time=time["trip_start_time"])
        tripStartTime.trip_id = trip.trip_id
        startTimeRows.append(tripStartTime)
        print tripStartTime.to_json

  db.session.add_all(startTimeRows)
  db.session.flush()
