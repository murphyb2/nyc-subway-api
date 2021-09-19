from datetime import timedelta, datetime
from django.conf import settings
import psycopg2

def shouldUpdate():
    # get today's date and find the previous Saturday
    DB_USER = settings.DB_USER
    DB_PASSWORD = settings.DB_PASSWORD
    DB_NAME = settings.DB_NAME
    DB_HOST = settings.DB_HOST

    result = {}
    print("should update check")

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        print("connected")
        cur = conn.cursor()

        today = datetime.today()
        day_of_week = today.isoweekday()
        
        if day_of_week == 6: # saturday
            day_of_week = -1
        if day_of_week == 7: # sunday
            day_of_week = 0

        saturday_obj = today - timedelta(days=(day_of_week + 1))
        saturday = saturday_obj.strftime("%Y-%m-%d")
        print(saturday)
        
        # find the most recent record in the db
        sql = f"""
            select (CASE 
                WHEN max(observed_at) IS NULL 
                THEN date('2019-1-04') 
                ELSE max(observed_at)
                END) from turnstile_observations;
        """
        cur.execute(sql)
        res = cur.fetchone()[0]
        
        db_most_recent_saturday_obj = res
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