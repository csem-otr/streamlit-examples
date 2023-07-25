import streamlit as st
import boto3

def get_s3():
    s3 = boto3.resource('s3', aws_access_key_id=st.secrets['AWS']['ACCESS_KEY'], aws_secret_access_key=st.secrets['AWS']['SECRET_ACCESS_KEY'])  
    return s3

def save_file(fl):
    file_name = fl.name
    s3 = get_s3()
    s3.Bucket(st.secrets['bucket_name']).put_object(Key=file_name, Body=fl)
    st.write('Success! File Saved!')

def get_files_list():
    s3= get_s3()
    file_names = []
    bucket = s3.Bucket(st.secrets['bucket_name'])
    for s3_obj in bucket.objects.all():
        file_names.append(s3_obj.key)
    s3_filename = st.sidebar.radio('Select a file', file_names, index=0)
    return s3_filename

def get_file(s3_filename):
    s3 = get_s3()
    obj = s3.Object(st.secrets['bucket_name'], s3_filename)
    fl = obj.get()['Body'].read().decode('utf-8').split("\n")

    for l in fl: 
        st.write(l)

def main():
    st.markdown(
        "<h1 style='text-align: center; color: black;'>Welcome to the S3 Example</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: grey;'>powered by Digital Stack Program🚀</p>",
        unsafe_allow_html=True,
    )
    st.write("---")
    st.markdown(
        "This is a demo shows how Streamlit can interact with an S3 Bucket."
    )


    fl = st.sidebar.file_uploader('Upload new file:', accept_multiple_files=False)

    if fl is not None:
        save_file(fl)

    s3_filename = get_files_list()

    if st.sidebar.button('Get File - ' + s3_filename):
        get_file(s3_filename)

if __name__ == '__main__':
    st.set_page_config(page_title="s3 Example", layout="wide", initial_sidebar_state="expanded")
    main()