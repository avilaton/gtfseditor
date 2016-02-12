from flask import (send_from_directory,
                   render_template,
                   request,
                   flash,
                   redirect, url_for)
from flask.views import MethodView
from flask.ext.login import login_required

from app.editor import editor
from app import db
from app.editor.forms import AgencyForm
from app.models import Agency
from app.utils import flash_errors


@editor.route('/')
@login_required
def root():
    return send_from_directory(editor.static_folder, 'index.html')


class AgenciesView(MethodView):

    @login_required
    def get(self):
        agencies = Agency.query.order_by(Agency.agency_name)
        return render_template('agencies/list.html', agencies=agencies)


class AgencyView(MethodView):

    @login_required
    def get(self, agency_id):
        agency = Agency.query.get(agency_id)
        return render_template('agencies/detail.html', agency=agency)


class AgencyEditView(MethodView):

    @login_required
    def get(self, agency_id):
        if agency_id:
            agency = Agency.query.get(agency_id)
        else:
            agency = None
        form = AgencyForm(request.form, agency, csrf_enabled=False)
        return render_template('agencies/form.html', form=form, agency=agency)

    @login_required
    def post(self, agency_id):
        if agency_id:
            agency = Agency.query.get(agency_id)
        else:
            agency = Agency()
            db.session.add(agency)
        form = AgencyForm(request.form, agency, csrf_enabled=False)

        if form.validate_on_submit():
            form.populate_obj(agency)
            db.session.commit()
            flash('Agency updated.', 'success')
            return redirect(url_for('editor.agencies'))

        return render_template('agencies/form.html', form=form, agency=agency)

    @login_required
    def delete(self, agency_id):
        agency = Agency.query.get(agency_id)
        if agency:
            db.session.delete(agency)
            db.session.commit()
            flash('Agency deleted.', 'success')
            return redirect(url_for('editor.agencies'))
        else:
            return redirect(url_for('editor.agencies'))



agencies_view = AgenciesView.as_view('agencies')
editor.add_url_rule('/agencies', view_func=agencies_view)

agency_view = AgencyView.as_view('agency')
editor.add_url_rule('/agencies/<agency_id>', view_func=agency_view)

agency_edit_view = AgencyEditView.as_view('agency_edit')
editor.add_url_rule('/agencies/<agency_id>/edit', view_func=agency_edit_view)
editor.add_url_rule('/agencies/new', defaults={'agency_id': None}, view_func=agency_edit_view)
