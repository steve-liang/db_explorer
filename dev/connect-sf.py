import snowflake.connector
import os

conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            database='RAW_ANALYTICS',
            schema='DEV_SLIANG',
            warehouse='LOADING',
            session_parameters={
                 'QUERY_TAG': 'test',
            }
        )

cur = conn.cursor()

# try:
#     cur.execute("SELECT * FROM weekly_statistics ORDER BY date_week")
#     for cols in cur:
#         print('{0}'.format(cols))
# finally:
#     cur.close()


import pandas as pd

def fetch_pandas_old(cur, sql):
    cur.execute(sql)
    rows = 0
    while True:
        dat = cur.fetchmany(50000)
        if not dat:
            break
        df = pd.DataFrame(dat, columns=cur.description)
        rows += df.shape[0]
    print(df)

# import pandas as pd
# 
# def fetch_pandas_sqlalchemy(sql):
#     rows = 0
#     for chunk in pd.read_sql_query(sql, engine, chunksize=50000):
#         rows += chunk.shape[0]
#     print(rows)

fetch_pandas_old(cur, 'SELECT date_week, starts, stops FROM WEEKLY_STATISTICS')