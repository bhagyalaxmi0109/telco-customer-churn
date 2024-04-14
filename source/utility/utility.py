import pandas as pd
import boto3
import os
from io import BytesIO
from datetime import datetime
from source.exception import ChurnException
global_timestamp = None


def generate_global_timestamp():

    global global_timestamp

    if global_timestamp is None:
        global_timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

    return global_timestamp


def export_data_csv(data, filename, file_path):

    try:

        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)

        data.to_csv(os.path.join(file_path, filename), index=False)

    except ChurnException as e:
        raise e


def import_csv_file(filename, file_path):
    try:

        if os.path.exists(file_path):

            return pd.read_csv(file_path + "\\" + filename)

    except ChurnException as e:
        print(f"path does not exist: {file_path}")
        raise e


def upload_artifact_to_s3(df, filename, file_path, bucket_name):
    try:
        s3_client = boto3.client()

        try:
            s3_client.head_bucket(Bucket=bucket_name)

        except ClientError as e:
            if e.response['Error']['Code']=='404':
                raise ChurnException(f"S3 bucket {bucket_name} does not exists")
            else:
                raise e
        csv_data = df.to_csv(index=False)

        s3_bucket_key = f"{file_path}/{filename}"
        s3_object_key = s3_object_key.replace("\\","/")
        s3_client.put_object (Bucket=bucket_name,key=s3_object_key, Body =csv_data)
    except ChurnException as e:
        raise e

def read_csv_from_s3(bucket_name, file_key):
    try:
        s3_client = boto3.client('s3')

        file_key=file_key.replace("\\","/")
        response = s3_client.get_object(Bucket=bucket_name,key=file_key)
        content = response['Body'].read()
        df = pd.read_csv(BytesIO(content))
        return df
    except ChurnException as e:
        raise e
