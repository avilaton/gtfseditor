#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import transitfeed

from server import engine
from server.models import Route
from server.models import Agency
from server.models import Trip

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

Session = sessionmaker(bind=engine)
db = scoped_session(Session)

class Feed(object):
  """docstring for Feed"""
  def __init__(self, arg):
    self.arg = arg
    self.schedule = transitfeed.Schedule()

  def __repr__(self):
    return 'a feed' 

  def build(self):
    self.loadAgencies()
    self.schedule.WriteGoogleTransitFeed('tmp/test.zip')

  def loadAgencies(self):
    logger.info("Loading Agencies")

    for row in db.query(Agency).all():
      agency = self.schedule.AddAgency(row.agency_name, row.agency_url, 
          row.agency_timezone, agency_id=row.agency_id)
      agency.agency_phone = row.agency_phone
      agency.agency_lang = row.agency_lang
    self.schedule.SetDefaultAgency(self.schedule.GetAgencyList()[0])