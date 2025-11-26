import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image

s3_client = boto3.client('s3')

# Destination bucket
DEST_BUCKET = 'amzn-s3-cc-destination'

def convert_to_bw(image_path, output_path):
    with Image.open(image_path) as image:
        # "L" = grayscale (8-bit pixels, black and white)
        bw_image = image.convert('L')
        bw_image.save(output_path)

def lambda_handler(event, context):
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']      
        key = unquote_plus(record['s3']['object']['key'])
        
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/bw-{}'.format(tmpkey)

        # Download file from source bucket
        s3_client.download_file(source_bucket, key, download_path)

        # Convert image to black and white
        convert_to_bw(download_path, upload_path)

        # Upload on destination bucket, keeping the same file name, adding a 'bw' prefix
        s3_client.upload_file(upload_path, DEST_BUCKET, f'bw-{key}')