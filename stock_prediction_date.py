from datetime import datetime, timedelta


def get_next_trading_day(date=None):
    if date:
        current_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        current_date = datetime.today()

    weekday = current_date.weekday()

    # Saturday → Monday
    if weekday == 5:
        next_day = current_date + timedelta(days=2)

    # Sunday → Monday
    elif weekday == 6:
        next_day = current_date + timedelta(days=1)

    # Weekday → same day (or next if needed)
    else:
        next_day = current_date

    return {
        "date": next_day.strftime("%Y-%m-%d"),
        "day": next_day.strftime("%A")
    }