from flask import send_from_directory, current_app

from flask.ext.login import login_required
from . import ng_editor


@ng_editor.route('/')
@login_required
def root():
    return send_from_directory(ng_editor.static_folder, 'index.html')


@ng_editor.route('/styles/<path:filename>')
def app_syles(filename):
    if current_app.config['DEBUG']:
        return send_from_directory(ng_editor.static_folder + '/../.tmp/styles/', filename)
    else:
        return send_from_directory(ng_editor.static_folder + '/styles/', filename)



@ng_editor.route('/bower_components/<path:filename>')
def bower_components(filename):
    return send_from_directory(ng_editor.static_folder + '/../bower_components/', filename)
