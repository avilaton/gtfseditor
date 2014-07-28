#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server import engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

Session = sessionmaker(bind=engine)
db = scoped_session(Session)

from server.services.interpolation import Interpolator
from server.services.populator import Populator

def generate_interpolated_stop_times():
    interpolator = Interpolator()
    # interpolator.bySpeed(trip_id='10.ida')
    interpolator.allSeqs()

def generate_stop_times_from_stop_seqs():
    populator = Populator()
    # populator.stop_seq_to_stop_times(trip_id='10.ida', commit=True)
    populator.allSeqs()


if __name__ == '__main__':
    # generate_interpolated_stop_times()
    generate_stop_times_from_stop_seqs()