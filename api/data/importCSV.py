import os
from django.conf import settings
import psycopg2
import pandas as pd


def importCSV(DATE):

    print("downloading data for " + DATE)

    DB_USER = settings.DB_USER
    DB_PASSWORD = settings.DB_PASSWORD
    DB_NAME = settings.DB_NAME
    DB_HOST = settings.DB_HOST
    result = {}
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        print("connected")
        cur = conn.cursor()

        # download new data
        url = f"http://web.mta.info/developers/data/nyct/turnstile/turnstile_{DATE}.txt"
        data = pd.read_csv(url)

        # create temp table to import new data
        sql = f"""
            DROP TABLE IF EXISTS csv_{DATE};

            CREATE TABLE csv_{DATE} (
                controlarea varchar,
                remoteunit varchar,
                subunit_channel_position varchar,
                station varchar,
                linenames varchar,
                division varchar,
                date varchar,
                time varchar,
                description varchar,
                entries integer,
                exits integer
            );
        """
        cur.execute(sql)
        print("tmp table created")

        # copy new data into temp table
        DIR = f"./{DATE}.csv"
        data.to_csv(DIR, index=False)
        sql = f"COPY csv_{DATE} FROM STDIN DELIMITER ',' CSV HEADER"
        cur.copy_expert(sql, open(f"{DIR}", "r"))
        os.remove(DIR)
        print("data copied into tmp table")

        # write new data from temp table to turnstile_observations and drop temp table
        sql = f"""INSERT INTO turnstile_observations
            SELECT * FROM (
            SELECT
                DISTINCT CONCAT(controlarea, remoteunit, subunit_channel_position, TO_TIMESTAMP(EXTRACT(EPOCH FROM (date || ' ' || time)::timestamp at time zone 'America/New_York'))) AS id,
                CONCAT(controlarea, remoteunit, subunit_channel_position) AS unit_id,
                controlarea,
                remoteunit,
                subunit_channel_position,
                station,
                linenames,
                division,
                TO_TIMESTAMP(EXTRACT(EPOCH FROM (date || ' ' || time)::timestamp at time zone 'America/New_York')) AS observed_at,
                description,
                entries,
                exits,
                NULL::bigint as net_entries,
                NULL::bigint as net_exits
            FROM csv_{DATE}
            ) a
            ORDER BY unit_id, observed_at
            ON CONFLICT (id) DO NOTHING;

            DROP TABLE csv_{DATE};
        """
        cur.execute(sql)
        
        print("turnsilte observations written")

        conn.commit()
        result["success"] = True
        result["error"] = ""
        result["status"] = 200
    except Exception as err:
        result["success"] = False
        result["error"] = str(err)
        result["status"] = 500
    finally:
        print("closing connection")
        cur.close()
        conn.close()
    
    return result