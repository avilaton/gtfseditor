import factory
from faker import Factory

from app import db
from app.models import Stop

faker = Factory.create()


class StopFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Stop
        sqlalchemy_session = db.session

    stop_lat = factory.LazyAttribute(lambda x: faker.latitude())
    stop_lon = factory.LazyAttribute(lambda x: faker.longitude())

