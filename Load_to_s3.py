
import boto3
from botocore.exceptions import ClientError
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

import os


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

logging.info("Starting uploading gaceta in s3 bucket")
gaceta_list = os.listdir('gacetas')

for gaceta in gaceta_list:
    logging.info("uploading file: "+gaceta)
    path = "gacetas/"+gaceta
    file_uploaded = upload_file(path, 'gacetas', object_name=gaceta)
    if file_uploaded:
        logging.info("file "+gaceta+" uploaded!")
        print("-"*20)
    else:
        logging.warning("file "+gaceta+" worng loaded")

logging.info("Loaded Finished")