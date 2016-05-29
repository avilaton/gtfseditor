from flask import (render_template,
                   request,
                   flash,
                   redirect, url_for)
from flask.views import MethodView
from flask.ext.login import login_required

from app.routes import routes_bp
from app import db
from app.routes.forms import RouteForm
from app.models import Route, Trip
from app.utils import flash_errors


class RoutesView(MethodView):

    @login_required
    def get(self):
        collection = Route.query.order_by(Route.route_short_name)
        return render_template('routes/list.html', collection=collection)


class RouteView(MethodView):

    @login_required
    def get(self, route_id):
        model = Route.query.get(route_id)
        trips = Trip.query.filter_by(route_id=route_id)\
                    .order_by(Trip.card_code, Trip.direction_id,
                              Trip.trip_headsign)
        return render_template('routes/detail.html', model=model, trips=trips)


class RouteEditView(MethodView):

    @login_required
    def get(self, route_id):
        if route_id:
            model = Route.query.get(route_id)
        else:
            model = None
        form = RouteForm(request.form, model, csrf_enabled=False)
        return render_template('routes/form.html', form=form, model=model)

    @login_required
    def post(self, route_id):
        if route_id:
            model = Route.query.get(route_id)
        else:
            model = Route()
            db.session.add(model)
        form = RouteForm(request.form, model, csrf_enabled=False)

        if form.validate_on_submit():
            form.populate_obj(model)
            db.session.commit()
            flash('Route updated.', 'success')
            return redirect(url_for('routes.index'))

        return render_template('routes/form.html', form=form, model=model)

    @login_required
    def delete(self, route_id):
        model = Route.query.get(route_id)
        if model:
            db.session.delete(model)
            db.session.commit()
            flash('Route deleted.', 'success')
            return redirect(url_for('routes.index'))
        else:
            return redirect(url_for('routes.index'))


class RouteDeleteView(MethodView):

    @login_required
    def get(self, route_id):
        model = Route.query.get(route_id)

        form = RouteForm(request.form, model, csrf_enabled=False)
        return render_template('routes/delete.html', form=form, model=model)

    @login_required
    def post(self, route_id):
        model = Route.query.get(route_id)
        if model:
            db.session.delete(model)
            db.session.commit()
            flash('Route deleted.', 'success')
            return redirect(url_for('routes.index'))
        else:
            return redirect(url_for('routes.index'))



index = RoutesView.as_view('index')
routes_bp.add_url_rule('/', view_func=index)

view_view = RouteView.as_view('view')
routes_bp.add_url_rule('/<route_id>', view_func=view_view)

edit_view = RouteEditView.as_view('edit')
routes_bp.add_url_rule('/<route_id>/edit', view_func=edit_view)
routes_bp.add_url_rule('/new', defaults={'route_id': None}, view_func=edit_view)

delete_view = RouteDeleteView.as_view('delete')
routes_bp.add_url_rule('/<route_id>/delete', view_func=delete_view)
