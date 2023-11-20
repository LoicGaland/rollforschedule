import calendar
from datetime import datetime

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


@date_picker.route('/my_schedule')
def my_schedule():
    now = datetime.now()
    month = calendar.month_name[now.month]
    c = calendar.Calendar()
    iter_days = c.itermonthdays3(now.year, now.month)
    before_month_days = []
    after_month_days = []
    month_days = []
    for date in iter_days:
        if date[:2] == (now.year, now.month):
            month_days.append(date[2])
        elif date[:2] < (now.year, now.month):
            before_month_days.append(date[2])
        else:
            after_month_days.append(date[2])

    return render_template(
        'my_schedule.html', month=month, year=now.year,
        before_month_days=before_month_days, after_month_days=after_month_days,
        month_days=month_days, active_day=now.day
    )
