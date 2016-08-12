# -*- coding: utf-8 -*-
"""Agency forms."""
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length, URL

from app.models import Agency


class AgencyForm(Form):
    """Register form."""

    agency_name = StringField('Name',
                           validators=[DataRequired(), Length(min=3, max=25)])
    agency_url = StringField('URL',
                        validators=[DataRequired(), URL()])
    agency_timezone = StringField('Timezone',
                        validators=[DataRequired()])
    agency_lang = StringField('Language',
                        validators=[DataRequired()])
    agency_phone = StringField('Phone',
                        validators=[DataRequired()])
