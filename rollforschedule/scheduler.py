import calendar
import json
from datetime import datetime, date

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import and_, text

from app import db
from models import Availability, Table


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
        year, month = get_year_and_month()

        calendar_configuration = get_calendar_configuration(year, month)
        player_availability = get_player_availability(current_user.id, year, month)

        return render_template(
            'my_schedule.html',
            calendar_configuration=calendar_configuration,
            player_availability=player_availability
        )
    

@scheduler.route("/table/<int:table_id>")
def table(table_id):
    table = Table.query.get_or_404(table_id)
    # TODO : query player's available days to compute days where playing this
    # table is possible, and display the results

    year, month = get_year_and_month()
    calendar_configuration = get_calendar_configuration(year, month)
    table_availability = get_table_availability(table_id, year, month)

    return render_template(
        'table.html',
        table=table,
        calendar_configuration=calendar_configuration,
        table_availability=table_availability
    )

def get_year_and_month():
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
    return year, month

def get_calendar_configuration(year, month):
    calendar_configuration = {
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "before_month_days": [],
        "after_month_days": [],
        "month_days": []
    }

    # Get all days for a monthly calendar starting on a monday and ending
    # on a sunday
    c = calendar.Calendar()
    iter_days = c.itermonthdays3(year, month)

    # Sort days into lists for previous, current and following month
    for day in iter_days:
        if day[:2] == (year, month):
            calendar_configuration["month_days"].append(day[2])
        elif day[:2] < (year, month):
            calendar_configuration["before_month_days"].append(day[2])
        else:
            calendar_configuration["after_month_days"].append(day[2])

    # Get previous and next month for navigation
    if month == 1:
        calendar_configuration["prev_month"] = 12
        calendar_configuration["prev_year"] = year - 1
    else:
        calendar_configuration["prev_month"] = month - 1
        calendar_configuration["prev_year"] = year
    if month == 12:
        calendar_configuration["next_month"] = 1
        calendar_configuration["next_year"] = year + 1
    else:
        calendar_configuration["next_month"] = month + 1
        calendar_configuration["next_year"] = year

    return calendar_configuration

def get_player_availability(player_id, year, month):
    # Get availability previously selected by player if any
    player_availability = {
        "available_days": [],
        "unavailable_days": []
    }

    # Get player availability from db
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
    
    # Sort days into available/unavailable
    for day in availability:
        if day.available:
            player_availability["available_days"].append(day.day.day)
        else:
            player_availability["unavailable_days"].append(day.day.day)

    return player_availability

def get_table_availability(table_id, year, month):
    table_availability = {
        "available_days": [],
        "unavailable_days": []
    }

    last_month_day = calendar.monthrange(year, month)[1]
    month_range = (
        date(year, month, 1).strftime("%Y-%m-%d"),
        date(year, month, last_month_day).strftime("%Y-%m-%d")
    )
    
    # query for days where everyone is available
    query = text(
        f"""
            SELECT CAST(STRFTIME("%d", day) AS INT)
            FROM availability
            INNER JOIN player ON availability.player_id = player.id
            INNER JOIN table_player ON table_player.player_id = player.id
            WHERE table_id = {table_id}
                AND day BETWEEN '{month_range[0]}' and '{month_range[1]}'
                AND available = TRUE
            GROUP BY day
            HAVING COUNT(availability.player_id) = (
                SELECT COUNT(*)
                FROM table_player
                WHERE table_id = {table_id}
            )
        """
    )
    results = db.session.execute(query)
    table_availability["available_days"] = [row[0] for row in results]

    # query for days where at least one player is unavailable
    query = text(
        f"""
            SELECT DISTINCT CAST(STRFTIME("%d", day) AS INT)
            FROM availability
            INNER JOIN player ON availability.player_id = player.id
            INNER JOIN table_player ON table_player.player_id = player.id
            WHERE table_id = {table_id}
                AND day BETWEEN '{month_range[0]}' and '{month_range[1]}'
                AND available = FALSE
        """
    )
    results = db.session.execute(query)
    table_availability["unavailable_days"] = [row[0] for row in results]

    return table_availability