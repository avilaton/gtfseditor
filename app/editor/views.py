from flask import render_template
from flask_login import login_required

from app.editor import editor


@editor.route('/')
@login_required
def root():
    return render_template('index.html')


