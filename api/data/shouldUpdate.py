from datetime import timedelta, datetime
from django.conf import settings
import psycopg2

def shouldUpdate():
    # get today's date and find the previous Sunday
    DB_USER = settings.DB_USER
    DB_PASSWORD = settings.DB_PASSWORD
    DB_NAME = settings.DB_NAME
    DB_HOST = settings.DB_HOST

    result = {}

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        print("connected")
        cur = conn.cursor()

        today = datetime.today()
        day_of_week = today.isoweekday()
        # monday -> 1
        # sunday -> 7
        days_past_saturday = day_of_week % 7 + 1
        saturday_obj = today - timedelta(days=days_past_saturday)
        saturday = saturday_obj.strftime("%Y-%m-%d")
        print(saturday)
        
        # find the most recent record in the db
        sql = f"""
            select max(observed_at) from turnstile_observations
        """
        cur.execute(sql)
        db_most_recent_saturday_obj = cur.fetchone()[0] + timedelta(days=1)
        print(f"db most recent saturday = {db_most_recent_saturday_obj}")

        # if the max date in the db is earlier than the most recent sunday
        if(db_most_recent_saturday_obj < saturday_obj):
            print('we need to update')
            result["shouldUpdate"] = True
            result["currentSaturday"] = saturday_obj
            result["dbMostRecentSaturday"] = db_most_recent_saturday_obj
        else:
            result["shouldUpdate"] = False
            print('we are current')
        
    except Exception as err:
        print(err)
        result["error"] = str(err)
    finally:
        print("closing connection")
        cur.close()
        conn.close()
    
    return result