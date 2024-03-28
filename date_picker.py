import calendar
import json
from datetime import datetime, date

from flask import Blueprint, redirect, render_template, session, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField

from app import db
from models import Availability


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


@date_picker.route('/my_schedule', methods=['GET', 'POST'])
@login_required
def my_schedule():

    # Process and commit availability POST data
    if request.method == 'POST':
    
        availability_data = json.loads(request.data)
        year = int(availability_data["year"])
        month = int(availability_data["month"])
        player_id = current_user.id

        for availability_key in ["available", "unavailable"]:
            for day_num in availability_data[availability_key]:

                day=date(year, month, int(day_num))
                available = availability_key == "available"

                # Check if availability day already exists for current user
                availability = Availability.query.filter_by(
                    player_id=player_id,
                    day=day
                ).first()

                # If so update availability
                if availability:
                    availability.available = available

                # Else insert
                else:
                    availability = Availability(
                        player_id=player_id,
                        day=day,
                        available=available
                    )
                    db.session.add(availability)

        db.session.commit()
        
        return (
            json.dumps({'success':True}),
            200,
            {'ContentType':'application/json'}
        )

    # Display a calendar on which user can select (un)available days
    else:
        # Set calendar to current month
        # TODO : display calendar for other months
        now = datetime.now()
        month_name = calendar.month_name[now.month]
        c = calendar.Calendar()

        # Get all days for a monthly calendar starting on a monday and ending
        # on a sunday
        iter_days = c.itermonthdays3(now.year, now.month)
        before_month_days = []
        after_month_days = []
        month_days = []

        # Sort days into lists for previous, current and following month
        for day in iter_days:
            if day[:2] == (now.year, now.month):
                month_days.append(day[2])
            elif day[:2] < (now.year, now.month):
                before_month_days.append(day[2])
            else:
                after_month_days.append(day[2])

    return render_template(
        'my_schedule.html', month=now.month, month_name=month_name,
        year=now.year, before_month_days=before_month_days,
        after_month_days=after_month_days, month_days=month_days
    )