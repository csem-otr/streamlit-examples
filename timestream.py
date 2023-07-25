import time
import altair
import pandas as pd
import streamlit as st
import boto3


def main():
    client = boto3.client(
        'timestream-query',    
        aws_access_key_id=st.secrets['AWS']['ACCESS_KEY'],
        aws_secret_access_key=st.secrets['AWS']['SECRET_ACCESS_KEY'],
        region_name=st.secrets['AWS']['REGION'] if 'REGION' in st.secrets['AWS'] else 'eu-west-1'
    )

    first = True
    container = st.empty()

    while True:
        response = client.query(
            QueryString='SELECT time, (measure_value::double / 1000.0) as value FROM "%s"."%s" WHERE time between ago(100m) and now() and measure_name=\'%s\' ORDER BY time DESC LIMIT 50' % (st.secrets['TIMESTREAM']['DATABASE'], st.secrets['TIMESTREAM']['TABLE'], st.secrets['TIMESTREAM']['MEASURE_NAME']),
            MaxRows=50
        )

        dts = []
        measures = []
        for r in response["Rows"]:
            dts.append(r["Data"][0]["ScalarValue"])
            measures.append(r["Data"][1]["ScalarValue"])

        # st.write(dts)
        # return
        index = pd.DatetimeIndex(dts)
        data = pd.DataFrame({'timestamp': index, st.secrets['TIMESTREAM']['MEASURE_NAME']: measures})
        hover = altair.selection_single(
            fields=["timestamp"],
            nearest=True,
            on="mouseover",
            empty="none",
        )

        container.altair_chart(altair.Chart(data).mark_line().encode(
            x='timestamp:T',
            y= st.secrets['TIMESTREAM']['MEASURE_NAME'] + ':Q'
        ).interactive())

        time.sleep(2)

if __name__ == '__main__':
    st.set_page_config(page_title="s3 Example", layout="wide")
    main()