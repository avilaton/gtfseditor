from flask import send_from_directory
from flask.ext.login import login_required
from . import editor

@editor.route('/')
@login_required
def root():
	return send_from_directory(editor.static_folder, 'index.html')

