# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    query = StringField('search', validators=[DataRequired(), Length(min=4, max=100)],
        render_kw={'placeholder': 'Search'})
    
    submit = SubmitField('GO')
