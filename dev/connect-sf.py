import snowflake.connector
import os

import pandas as pd
import time

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

query = 'SELECT * FROM stg_starts order by date'
cur.execute(query)
def fetch_pandas_new(cur, sql):
    cur.execute(sql)

    dat = cur.fetchmany(10000)
    df = pd.DataFrame(dat, columns=[x[0] for x in cur.description])
    df = pd.DataFrame(dat)
    return(df)

t = time.time()
from_pd = fetch_pandas_new(cur, query)
elapsed = time.time() - t
print(elapsed)



def fetch_pandas_sqlalchemy(sql):
    rows = 0
    for chunk in pd.read_sql_query(sql, conn, chunksize=50000):
        rows += chunk.shape[0]
    return(chunk)

from_sql = fetch_pandas_sqlalchemy(query)

print(from_pd.equals(from_sql))