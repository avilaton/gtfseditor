from flask import send_from_directory
from flask.ext.login import login_required
from . import admin

@admin.route('/')
@login_required
def root():
	return send_from_directory(admin.static_folder, 'index.html')

