

def register_admin_views(admin):

    # admin views
    from .views import MyModelView
    from app.models import Agency
    from app.models import Route
    from app.models import Trip
    from app.models import Stop
    from app.models import StopTime
    from app.models import ShapePath
    from app import db


    admin.add_view(MyModelView(Agency, db.session))
    admin.add_view(MyModelView(Route, db.session))
    admin.add_view(MyModelView(Trip, db.session))
    admin.add_view(MyModelView(Stop, db.session))
    admin.add_view(MyModelView(StopTime, db.session))
    admin.add_view(MyModelView(ShapePath, db.session))
