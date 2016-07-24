import pytest
from app.models import Stop
from tests.factories import StopFactory
#
#
# def test_stops(client, session):
#     s = StopFactory()
#     session.commit()
#     res = client.get('/api/stops/')
#     assert res.status_code == 200


def test_stop_create(db, session):
    s = Stop(stop_name='test_stop')
    db.session.add(s)
    db.session.flush()
    print s, s.stop_name, s.stop_id

    stops = db.session.query(Stop).all()
    print stops

    assert False

def test_stop_create_2(db, session):
    s = Stop(stop_name='test_stop')
    s2 = Stop(stop_name='test_stop_2')
    db.session.add(s)
    db.session.add(s2)
    db.session.flush()
    print s, s.stop_name, s.stop_id
    print s2, s2.stop_name, s2.stop_id

    stops = session.query(Stop).all()
    print stops

    assert False
