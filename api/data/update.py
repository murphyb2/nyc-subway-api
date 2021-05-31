from django.conf import settings
import psycopg2
import time
from datetime import timedelta

def updateValues(beginDate):
    DB_USER = settings.DB_USER
    DB_PASSWORD = settings.DB_PASSWORD
    DB_NAME = settings.DB_NAME
    DB_HOST = settings.DB_HOST
    start_time = time.time()
    result = {}

    print("updating values")

    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        print("connected")
        cur = conn.cursor()
        # update net values
        sql = f"""
            SET work_mem = '256MB';
            WITH net_observations AS (
                SELECT
                id,
                entries - lag(entries, 1) OVER w AS calculated_net_entries,
                exits - lag(exits, 1) OVER w AS calculated_net_exits,
                DATE_PART('day', observed_at - lag(observed_at, 1) OVER w) * 24 + DATE_PART('hour', observed_at - lag(observed_at, 1) OVER w) as hours_difference
                FROM turnstile_observations
                WHERE observed_at >= '{beginDate.strftime("%Y-%m-%d")}'
                WINDOW w AS (PARTITION BY unit_id ORDER BY observed_at)
            )
            UPDATE turnstile_observations
            SET
            net_entries = CASE WHEN abs(calculated_net_entries) < 10000 AND hours_difference <= 24 THEN abs(calculated_net_entries) END,
            net_exits = CASE WHEN abs(calculated_net_exits) < 10000 AND hours_difference <= 24 THEN abs(calculated_net_exits) END
            FROM net_observations
            WHERE turnstile_observations.id = net_observations.id
            AND net_entries IS NULL;
        """
        cur.execute(sql)
        print("updated turnstile_observations")

        # update daily_subunit
        sql = f"""
            DROP TABLE IF EXISTS daily_subunit;
            CREATE TABLE daily_subunit AS (
            SELECT
                unit_id,
                (array_agg(remoteunit))[1] AS remoteunit,
                date_trunc('day', observed_at - interval '2h')::date AS date,
                SUM(net_entries) AS entries,
                SUM(net_exits) AS exits
            FROM turnstile_observations
            GROUP BY unit_id, date_trunc('day', observed_at - interval '2h')
            );
        """
        cur.execute(sql)
        print("updated daily_subunit")
        
        #  update daily_complex
        sql = f"""
            DROP table if exists daily_complex;
            CREATE TABLE daily_complex AS (
                SELECT
                complex_id,
                date,
                sum(entries) as entries,
                sum(exits) as exits
                FROM (
                SELECT
                CASE
                    WHEN unique_remotes.complex_id IS NULL
                    THEN remoteunit
                    ELSE unique_remotes.complex_id::text
                END,
                    remoteunit,
                date,
                entries,
                    exits
                FROM daily_subunit
                LEFT JOIN (
                SELECT DISTINCT ON (remote) * FROM remote_complex_lookup
                ) unique_remotes
                ON daily_subunit.remoteunit = unique_remotes.remote
            ) a
                GROUP BY complex_id, date
            )
        """
        cur.execute(sql)
        print("updated daily_complex")
        
        #  update year table
        
        sql = f"""
            DROP TABLE IF EXISTS daily_counts_{beginDate.year};
            CREATE TABLE daily_counts_{beginDate.year} AS (
            SELECT
                b.stop_name,
                b.daytime_routes,
                b.division,
                b.line,
                b.borough,
                b.structure,
                b.gtfs_longitude,
                b.gtfs_latitude,
                a.*
            FROM daily_complex a
            LEFT JOIN (
            SELECT
                DISTINCT ON (complex_id)
                complex_id,
                stop_name,
                daytime_routes,
                division,
                line,
                borough,
                structure,
                gtfs_longitude,
                gtfs_latitude
            FROM stations
            ) b
            ON a.complex_id = b.complex_id
            WHERE date >= '{beginDate.year}-01-01'::date
            AND date < '{beginDate.year + 1}-01-01'
            )
        """
        cur.execute(sql)
        print(f"updated {beginDate.year} table")

        conn.commit()

        # find the most recent record in the db
        sql = f"""
            select max(observed_at) from turnstile_observations
        """
        cur.execute(sql)
        new_most_recent_saturday_obj = cur.fetchone()[0]

        result['newMostRecentSaturday'] = new_most_recent_saturday_obj.strftime("%Y-%m-%d")
        result["success"] = True
        result["error"] = ""
        result["status"] = 200
        print("Successfully updated net values!")
    except Exception as ex:
        print(ex)
        result["success"] = False
        result["error"] = str(ex)
        result["status"] = 500
    except: 
        print('something else went wrong...')
    finally:
        print("closing connection")
        cur.close()
        conn.close()
    print(f"Elapsed time: {time.time() - start_time}")

    return result
    