import codecs


def readCsv(Model, filename, mode=None):
  print("Importing " + Model.__tablename__ + " from : " + filename)
  with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    if not mode:
      for row in reader:
        d = {field: (codecs.decode(row[field],'utf8') if row[field] else None)
          for field in reader.fieldnames}
        model = Model(**d)
        db.session.merge(model)
      db.session.commit()
    elif mode in ['direct']:
      db.engine.execute(Model.__table__.delete())
      insertStmt = Model.__table__.insert()
      db.engine.execute(insertStmt, [row for row in reader])


@manager.command
def importCsv(modelname, filename, mode=None):
  Model = globals()[modelname]
  readCsv(Model, filename, mode=mode)


@manager.command
def importCba(folder):
  """Usage:
  FLASK_CONFIG=local ./manage.py importCba <FOLDER>
  """

  importCsv("Agency", folder + "agency.csv")
  importCsv("Calendar", folder + 'calendar.csv')
  importCsv("CalendarDate", folder + 'calendar_dates.csv')
  importCsv("FareAttribute", folder + 'fare_attributes.csv')
  importCsv("FareRule", folder + 'fare_rules.csv')
  importCsv("FeedInfo", folder + 'feed_info.csv')
  importCsv("Route", folder + 'routes.csv')
  importCsv("RouteFrequency", folder + 'route_frequencies.csv')
  importCsv("Stop", folder + 'stops.csv')
  importCsv("Shape", folder + 'shapes.csv', mode='direct')
  importCsv("Trip", folder + 'trips.csv')
  importCsv("TripStartTime", folder + 'trips_start_times.csv')
  importCsv("StopSeq", folder + 'stop_seq.csv', mode='direct')
  importCsv("StopTime", folder + 'stop_times.csv')
  importCsv("Frequency", folder + 'frequencies.csv')
