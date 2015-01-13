from flask import Flask, jsonify, request, g, abort, url_for, current_app,render_template, send_from_directory
from . import admin


@admin.route('/index')
def root():
	return send_from_directory(admin.static_folder, 'index.html')

