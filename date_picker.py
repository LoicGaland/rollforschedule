from flask import Blueprint, redirect, render_template, session
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField


class InfoForm(FlaskForm):
    startdate = DateField(
        'Start Date',
        format='%Y-%m-%d',
        validators=(validators.DataRequired(),)
    )
    enddate = DateField(
        'End Date',
        format='%Y-%m-%d',
        validators=(validators.DataRequired(),)
    )
    submit = SubmitField('Submit')


date_picker = Blueprint('date_picker', __name__)


@date_picker.route('/date_selection', methods=['GET', 'POST'])
def date_selection():
    form = InfoForm()
    if form.validate_on_submit():
        session['startdate'] = form.startdate.data
        session['enddate'] = form.enddate.data
        return redirect('date_display')
    return render_template('date_selection.html', form=form)


@date_picker.route('/date_display', methods=['GET', 'POST'])
def date_display():
    startdate = session['startdate']
    enddate = session['enddate']
    return render_template('date_display.html')
