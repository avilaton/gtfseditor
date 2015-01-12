from flask import jsonify, request, g, abort, url_for, current_app,render_template
from . import admin

@admin.route('/admin/')
def admin():
	print "UUUUUUUUUU#############"
	return render_template('index.html')