#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app, request, url_for
from . import db

from flask.ext.login import UserMixin
from datetime import datetime
from . import login_manager

class Entity(object):
  @property
  def to_json(self):
    d = {}
    for column in self.__table__.columns:
      attr = getattr(self, column.name)
      if attr is not None:
        if isinstance(column.type, db.Float):
          d[column.name] = float(attr)
        elif isinstance(column.type, db.Boolean):
          d[column.name] = attr
        elif isinstance(column.type, db.Integer):
          d[column.name] = int(attr)
        else:
          d[column.name] = unicode(attr)
      else:
        d[column.name] = None
    return d

  def __repr__(self):
    info = ['<', self.__class__.__name__, ': ']
    for col in self.__table__.primary_key.columns:
      attr = getattr(self, col.name)
      info.extend([col.name, '=', unicode(attr), ' '])
    info.append('>')
    return ('').join(info)


class Route(db.Model, Entity):
  __tablename__ = 'routes'
  route_id = db.Column(db.Integer, primary_key=True)
  agency_id = db.Column(db.Integer)
  route_short_name = db.Column(db.String(50))
  route_long_name = db.Column(db.String(150))
  route_desc = db.Column(db.String(150))
  route_type = db.Column(db.String(50))
  route_color = db.Column(db.String(50))
  build_type = db.Column(db.String(50))
  route_text_color = db.Column(db.String(50))
  active = db.Column(db.Boolean, default=False)


class FeedInfo(db.Model, Entity):
  __tablename__ = 'feed_info'
  feed_publisher_name = db.Column(db.String(50), primary_key=True)
  feed_publisher_url = db.Column(db.String(50))
  feed_lang = db.Column(db.String(50))
  feed_version = db.Column(db.String(50))
  feed_start_date = db.Column(db.String(50))
  feed_end_date = db.Column(db.String(50))


class Agency(db.Model, Entity):
  __tablename__ = 'agency'
  agency_id = db.Column(db.Integer, primary_key=True)
  agency_name = db.Column(db.String(50))
  agency_url = db.Column(db.String(50))
  agency_timezone = db.Column(db.String(50))
  agency_lang = db.Column(db.String(50))
  agency_phone = db.Column(db.String(50))


class Calendar(db.Model, Entity):
  __tablename__ = 'calendar'
  service_id = db.Column(db.Integer, primary_key=True)
  service_name = db.Column(db.String(50))
  start_date = db.Column(db.String(50))
  end_date = db.Column(db.String(50))
  monday = db.Column(db.String(50))
  tuesday = db.Column(db.String(50))
  wednesday = db.Column(db.String(50))
  thursday = db.Column(db.String(50))
  friday = db.Column(db.String(50))
  saturday = db.Column(db.String(50))
  sunday = db.Column(db.String(50))


class Trip(db.Model, Entity):
  __tablename__ = 'trips'
  trip_id = db.Column(db.Integer, primary_key=True)
  route_id = db.Column(db.Integer, db.ForeignKey("routes.route_id"))
  service_id = db.Column(db.Integer)
  trip_headsign = db.Column(db.String(150))
  trip_short_name = db.Column(db.String(150))
  direction_id = db.Column(db.String(50))
  shape_id = db.Column(db.Integer)
  card_code = db.Column(db.String(50))
  active = db.Column(db.Boolean, default=False)


class CalendarDate(db.Model, Entity):
  __tablename__ = 'calendar_dates'
  service_id = db.Column(db.Integer, db.ForeignKey("calendar.service_id",
    onupdate="CASCADE"), primary_key=True)
  date = db.Column(db.String(50), primary_key=True)
  exception_type = db.Column(db.String(50), primary_key=True)


class FareAttribute(db.Model, Entity):
  __tablename__ = 'fare_attributes'
  fare_id = db.Column(db.Integer, primary_key=True)
  price = db.Column(db.String(50))
  currency_type = db.Column(db.String(50))
  payment_method = db.Column(db.String(50))
  transfers = db.Column(db.String(50))
  transfer_duration = db.Column(db.String(50))


class FareRule(db.Model, Entity):
  __tablename__ = 'fare_rules'
  fare_id = db.Column(db.Integer, primary_key=True)
  route_id = db.Column(db.Integer)
  origin_id = db.Column(db.String(50))
  destination_id = db.Column(db.String(50))
  contains_id = db.Column(db.String(50))


class Frequency(db.Model, Entity):
  __tablename__ = 'frequencies'
  trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id", onupdate="CASCADE"), primary_key=True)
  start_time = db.Column(db.String(50))
  end_time = db.Column(db.String(50))
  headway_secs = db.Column(db.Integer)
  exact_times = db.Column(db.String(50))


class RouteFrequency(db.Model, Entity):
  __tablename__ = 'route_frequencies'
  route_id = db.Column(db.Integer, db.ForeignKey("routes.route_id", onupdate="CASCADE"), primary_key=True)
  service_id = db.Column(db.Integer, db.ForeignKey("calendar.service_id",
    onupdate="CASCADE"), primary_key=True)
  start_time = db.Column(db.String(50), primary_key=True)
  end_time = db.Column(db.String(50), primary_key=True)
  headway_secs = db.Column(db.Integer)


class Shape(db.Model, Entity):
  __tablename__ = 'shapes'
  shape_id = db.Column(db.Integer, primary_key=True)
  shape_pt_lat = db.Column(db.Float(precision=53))
  shape_pt_lon = db.Column(db.Float(precision=53))
  shape_pt_time = db.Column(db.String(50))
  shape_pt_sequence = db.Column(db.Integer, primary_key=True)


class Stop(db.Model, Entity):
  __tablename__ = 'stops'
  stop_id = db.Column(db.Integer, primary_key=True)
  stop_code = db.Column(db.String(50))
  stop_desc = db.Column(db.String(250))
  stop_name = db.Column(db.String(250))
  stop_lat = db.Column(db.Float(precision=53))
  stop_lon = db.Column(db.Float(precision=53))
  stop_calle = db.Column(db.String(250))
  stop_numero = db.Column(db.String(50))
  stop_entre = db.Column(db.String(250))
  stop_esquina = db.Column(db.String(250))


class StopSeq(db.Model, Entity):
  __tablename__ = 'stop_seq'
  trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id",
    onupdate="CASCADE"), primary_key=True)
  stop_id = db.Column(db.Integer, db.ForeignKey("stops.stop_id",
    onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
  stop_sequence = db.Column(db.Integer, primary_key=True) 
  stop_time = db.Column(db.String(50)) 
  shape_dist_traveled = db.Column(db.Float(precision=53))


class StopTime(db.Model, Entity):
  __tablename__ = 'stop_times'
  trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id", onupdate="CASCADE"), primary_key=True)
  stop_id = db.Column(db.Integer, db.ForeignKey("stops.stop_id",
    onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
  stop_sequence = db.Column(db.Integer, primary_key=True)
  arrival_time = db.Column(db.String(50))
  departure_time = db.Column(db.String(50))
  shape_dist_traveled = db.Column(db.Float(precision=53))


class Transfer(db.Model, Entity):
  __tablename__ = 'transfers'
  from_stop_id = db.Column(db.Integer, primary_key=True)
  to_stop_id = db.Column(db.Integer)
  transfer_type = db.Column(db.String(50))


class TripStartTime(db.Model, Entity):
  __tablename__ = 'trips_start_times'
  trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id", onupdate="CASCADE"), primary_key=True)
  service_id = db.Column(db.Integer, db.ForeignKey("calendar.service_id",
    onupdate="CASCADE"), primary_key=True)
  start_time = db.Column(db.String(50), primary_key=True)


class Permission:
    COMMENT = 0x01
    EDIT_TIMES = 0x02
    EDIT_ROUTES = 0x04
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.COMMENT | Permission.EDIT_TIMES | True),
            'Agency': (Permission.COMMENT, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column(db.DateTime(), default=datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self  ,password , email):
        super(User, self).__init__(**kwargs)
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0x80).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.email)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

