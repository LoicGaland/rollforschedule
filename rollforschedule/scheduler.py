import calendar
import json
from datetime import datetime, date

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app import db
from models import Availability


scheduler = Blueprint('date_picker', __name__)


@scheduler.route('/my_schedule', methods=['GET', 'POST'])
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

                day = date(year, month, int(day_num))
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
            json.dumps({'success': True}),
            200,
            {'ContentType': 'application/json'}
        )

    # Display a calendar on which user can select (un)available days
    else:
        # Get year and month from parameters or default to current
        year = request.args.get('year')
        month = request.args.get('month')
        if not (month and year):
            now = datetime.now()
            year = now.year
            month = now.month

        # Set calendar to month
        month_name = calendar.month_name[month]
        c = calendar.Calendar()

        # Get all days for a monthly calendar starting on a monday and ending
        # on a sunday
        iter_days = c.itermonthdays3(year, month)
        before_month_days = []
        after_month_days = []
        month_days = []

        # Sort days into lists for previous, current and following month
        for day in iter_days:
            if day[:2] == (year, month):
                month_days.append(day[2])
            elif day[:2] < (year, month):
                before_month_days.append(day[2])
            else:
                after_month_days.append(day[2])

    return render_template(
        'my_schedule.html', month=month, month_name=month_name,
        year=year, before_month_days=before_month_days,
        after_month_days=after_month_days, month_days=month_days
    )


@scheduler.route('/scheduling')
@login_required
def scheduling():
    pass
