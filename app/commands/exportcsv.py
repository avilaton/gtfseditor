
import csv


class DictUnicodeProxy(object):
  def __init__(self, d):
    self.d = d
  def __iter__(self):
    return self.d.__iter__()
  def get(self, item, default=None):
    i = self.d.get(item, default)
    if isinstance(i, unicode):
      return i.encode('utf-8')
    return i



def exportToCsv(Model, filename, mode=None):
  print("Exporting " + Model.__tablename__ + " to : " + filename)
  with open(filename + Model.__tablename__ + ".csv", 'w') as csvfile:
    fieldnames = Model.__table__.columns.keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in Model.query.all():
      writer.writerow(DictUnicodeProxy(row.to_json))



@manager.command
def export(folder=".tmp/export/"):

  exportToCsv(Agency, folder)
  exportToCsv(Calendar, folder)
  exportToCsv(CalendarDate, folder)
  exportToCsv(FareAttribute, folder)
  exportToCsv(FareRule, folder)
  exportToCsv(FeedInfo, folder)
  exportToCsv(RouteFrequency, folder)
  exportToCsv(Route, folder)
  exportToCsv(Stop, folder)
  exportToCsv(Shape, folder)
  exportToCsv(Trip, folder)
  exportToCsv(TripStartTime, folder)
  exportToCsv(StopSeq, folder)
  exportToCsv(StopTime, folder)
  exportToCsv(Frequency, folder)
