from flask import (send_from_directory,
                   render_template,
                   request,
                   flash,
                   redirect, url_for)
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

@editor.route('/agencies')
@login_required
def list_agencies():
    agencies = Agency.query.order_by(Agency.agency_name).all()
    return render_template('agencies/list.html', agencies=agencies)

@editor.route('/agencies/new', methods=['GET', 'POST'])
@editor.route('/agencies/<agency_id>', methods=['GET', 'POST'])
@login_required
def create_or_edit_agency(agency_id=None):
    if agency_id:
        agency = Agency.query.get(agency_id)
    else:
        agency = None
    form = AgencyForm(request.form, agency, csrf_enabled=False)

    if form.validate_on_submit():
        if not agency:
            agency = Agency()
            db.session.add(agency)
            flash('Agency created.', 'success')
        else:
            flash('Agency updated.', 'success')
        form.populate_obj(agency)
        db.session.commit()
        return redirect(url_for('editor.list_agencies'))

    return render_template('agencies/form.html', form=form, agency=agency)

@editor.route('/agencies/<int:agency_id>/delete')
@login_required
def delete_agency(agency_id):
    agency = Agency.query.get(agency_id)
    if agency:
        db.session.delete(agency)
        db.session.commit()
        flash('Agency deleted.', 'success')
        return redirect(url_for('editor.list_agencies'))
    else:
        return redirect(url_for('editor.list_agencies'))
