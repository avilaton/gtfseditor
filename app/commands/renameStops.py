
@manager.command
def renamestops():
  """Creates stop names from other columns"""

  stops = Stop.query.all()
  total = len(stops)

  for i, stop in enumerate(stops):
    stop.stop_calle = stop.stop_calle.title()
    stop_name = ' '.join([stop.stop_calle, stop.stop_numero]).strip()
    if not stop_name:
      stop_name = stop.stop_id
    stop.stop_name = stop_name
    db.session.merge(stop)
    print("{2}/{1} Stop_id: {0} renamed to: {3}".format(stop.stop_id, total, i, stop_name.encode('utf8')))
  db.session.commit()

