import logging
import math
import os
import time
import boto3
import streamlit as st


LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

client = boto3.client(
        'timestream-write',    
        aws_access_key_id=st.secrets['AWS']['ACCESS_KEY'],
        aws_secret_access_key=st.secrets['AWS']['SECRET_ACCESS_KEY'],
    )

if __name__ == '__main__':
    i = 0

    while True:
        ibi = 1000 + 100 * math.sin(float(i) / 9 * 2 * math.pi)
        CURRENT_TIME = str(int(time.time() * 1000))

        logging.info("Timestream database: %s" % st.secrets['TIMESTREAM']['DATABASE'])
        logging.info("Timestream table: %s" % st.secrets['TIMESTREAM']['TABLE'])
        logging.info("Writing ibi %s to database" % ibi)
        client.write_records(
            DatabaseName=st.secrets['TIMESTREAM']['DATABASE'],
            TableName=st.secrets['TIMESTREAM']['TABLE'],
            Records=[{
                'Dimensions': [
                    {
                        'Name': 'type',
                        'Value': st.secrets['TIMESTREAM']['MEASURE_NAME'],
                        'DimensionValueType': 'VARCHAR'
                    },
                ],
                'MeasureName': st.secrets['TIMESTREAM']['MEASURE_NAME'],
                'MeasureValue': "%s" % ibi,
                'MeasureValueType': 'DOUBLE',
                'Time': CURRENT_TIME,
            }]
        )
        i += 1
        time.sleep(ibi / 1000)
            # st.secrets['TIMESTREAM']['MEASURE_NAME']