import flask_login
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask import redirect, url_for, request, current_app

# from ..models.permision import Permission

# Create customized model view class
class MyModelView(ModelView):

    def is_accessible(self):
        print 'hello'
        return flask_login.current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        return current_app.login_manager.unauthorized()
        # return redirect(url_for('login', next=request.url))


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not flask_login.current_user.is_authenticated():
            return current_app.login_manager.unauthorized()
        else:
            if not flask_login.current_user.can(0x80):
                return current_app.login_manager.unauthorized()
        return super(MyAdminIndexView, self).index()


