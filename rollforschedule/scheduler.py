import calendar
import json
from datetime import datetime, date

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import and_

from app import db
from models import Availability


scheduler = Blueprint('scheduler', __name__)

# Personal schedule route, where user select which dates they are available at.
# Those (un)available dates are then POSTed and stored in DB.
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

        # Remove unset availability in case they were previously set as
        # (un)available
        for day_num in availability_data["unset"]:

            day = date(year, month, int(day_num))
            Availability.query.filter_by(
                player_id=player_id,
                day=day
            ).delete()

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
        else:
            year = int(year)
            month = int(month)

        # Get availability previously selected by user if any
        availability = get_player_availability(current_user.id, year, month)
        available_days = []
        unavailable_days = []
        for day in availability:
            if day.available:
                available_days.append(day.day.day)
            else:
                unavailable_days.append(day.day.day)

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

        # Get previous and next month for navigation
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

    return render_template(
        'my_schedule.html', month=month, month_name=month_name,
        year=year, before_month_days=before_month_days,
        after_month_days=after_month_days, month_days=month_days,
        prev_month=prev_month, prev_year=prev_year, next_month=next_month,
        next_year=next_year, available_days=available_days,
        unavailable_days=unavailable_days
    )




def get_player_availability(player_id, year, month):
    last_month_day = calendar.monthrange(year, month)[1]

    availability = Availability.query.filter(
        and_(
            Availability.player_id==player_id,
            Availability.day.between(
                date(year, month, 1),
                date(year, month, last_month_day)
            )
        )
    ).all()

    return availability
