from flask import send_from_directory
from . import admin

@admin.route('/')
def root():
	return send_from_directory(admin.static_folder, 'index.html')

