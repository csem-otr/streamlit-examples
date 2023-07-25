# Streamlit + AWS Examples

There are currently two examples:
 - s3 example - allowing you to upload a file and listing all uploaded files
 - timestream example - Shows an updating graph of time series data

Create a user on AWS and get the access and secret access key and put them in .streamlit/secrets.toml (see .streamlit/secrets.example.toml)

Create a bucket b1 and make sure the user has read/write access on the bucket, then add the bucket name to .streamlit/secrets.toml.

Create a timestreams database and give permissions to timestream:DescribeEndpoints on "*" and read/write on the database and its table. Then add the table, db and 

## Local deployment
```
# Install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# S3 example
streamlit run s3.py

# Timestream example
LOGLEVEL=INFO python timestream_feeder.py # Let run in another terminal
streamlit run timestream.py
```

## Cloud deployment
For 