# -*- coding: utf-8 -*-
"""Agency forms."""
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models import Agency


class AgencyForm(Form):
    """Register form."""

    agency_name = StringField('Name',
                           validators=[DataRequired(), Length(min=3, max=25)])
    agency_url = StringField('URL',
                        validators=[DataRequired()])
    agency_timezone = StringField('Timezone',
                        validators=[DataRequired()])
    agency_lang = StringField('Language',
                        validators=[DataRequired()])
    agency_phone = StringField('Phone',
                        validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(AgencyForm, self).__init__(*args, **kwargs)
        # self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(AgencyForm, self).validate()
        if not initial_validation:
            return False
        # user = User.query.filter_by(username=self.username.data).first()
        # if user:
        #     self.username.errors.append('Username already registered')
        #     return False
        # user = User.query.filter_by(email=self.email.data).first()
        # if user:
        #     self.email.errors.append('Email already registered')
        #     return False
        return True
