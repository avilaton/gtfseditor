
import os
import unicodecsv as csv
from app.models import *


def exportToCsv(Model, filename, mode=None):
    print("Exporting " + Model.__tablename__ + " to : " + filename)
    with open(filename + Model.__tablename__ + ".csv", 'wb') as csvfile:
        fieldnames = Model.__table__.columns.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in Model.query.all():
            writer.writerow(row.to_json)


from flask_script import Command, Option
from flask_script.commands import InvalidCommand


class ExportCSV(Command):
    """Exports tables to CSV"""

    def get_options(self):
        return [
            Option('-d', '--destination', dest='destination', default='.tmp/export/')
        ]

    def run(self, destination=False):
        if not os.path.isdir(destination):
            os.makedirs(destination)

        exportToCsv(Agency, destination)
        exportToCsv(Calendar, destination)
        exportToCsv(CalendarDate, destination)
        exportToCsv(FareAttribute, destination)
        exportToCsv(FareRule, destination)
        exportToCsv(FeedInfo, destination)
        exportToCsv(RouteFrequency, destination)
        exportToCsv(Route, destination)
        exportToCsv(Stop, destination)
        exportToCsv(ShapePath, destination)
        exportToCsv(Trip, destination)
        exportToCsv(TripStartTime, destination)
        exportToCsv(StopSeq, destination)
        exportToCsv(StopTime, destination)
        exportToCsv(Frequency, destination)

