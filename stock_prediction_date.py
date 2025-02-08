from datetime import datetime , timedelta

def trading_day(date=None):
    if date:
        today_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        today_date = datetime.today()
    
    week_day = today_date.weekday()   # return no of day in week saturday = 5 , sunday = 6 , monday = 0
    
    if week_day == 5:
        next_trading_day = today_date + timedelta(days=2)

    elif week_day == 6:
        next_trading_day = today_date + timedelta(days=1)
    
    else:
        next_trading_day = today_date

    

    return next_trading_day.strftime("%A")