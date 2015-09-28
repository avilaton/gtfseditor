
# legacy
@manager.command
def importCardCodes(filename):
  """Creates stop names from other columns"""
  import csv

  with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      codigo = row["codigo"].strip()
      trip_id = row["trip_id"].strip()
      card_code = codigo[-3:]
      route_id = codigo[:-3]
      if route_id.isdigit():
        route_id = route_id.zfill(3)
      trip = Trip.query.filter_by(trip_id=trip_id).first()
      print codigo, card_code, trip_id, trip
      if trip:
        trip.card_code = card_code
        db.session.merge(trip)
  db.session.commit()
