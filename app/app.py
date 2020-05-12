from typing import final
import streamlit as st

import snowflake.connector as sf
import os
import pandas as pd
import numpy as np

st.write("SnowflakeDB Explorer")


class SnowflakeDB(object):
    def __init__(self):
        self._db_connection = sf.connect(
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
        self.cur = self._db_connection.cursor()

    def query(self, query, params):
        return self._db_cur.execute(query, params)

    def __del__(self):
        self._db_connection.close()

try:
    conn = SnowflakeDB()

    conn.query = st.text_input('SQL Query',  'SELECT date_week, starts, stops FROM WEEKLY_STATISTICS order by date_week')
    
    @st.cache(hash_funcs={sf.cursor.SnowflakeCursor: id}, allow_output_mutation=True)
    def fetch_pandas(cur, sql):
        cur.execute(sql)
        dat = cur.fetchmany(10000)
        df = pd.DataFrame(dat, columns=[x[0] for x in cur.description])
        return(df)

    
    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    
    # Load 10,000 rows of data into the dataframe.
    data = fetch_pandas(conn.cur, conn.query)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text("Done! (using st.cache)")
    
    
    '''
    Results:
    '''
    st.write(data)

except Exception as e: 
    st.write(e)

