import json
import boto3

s3 = boto3.client("s3")

def cors_headers():
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*", 
        "Access-Control-Allow-Headers": "Authorization,Content-Type",
        "Access-Control-Allow-Methods": "GET,OPTIONS",
    }


def lambda_handler(event, context):
    bucket_name = event["pathParameters"]["bucket"]
    file_name = event["queryStringParameters"]["file"]
    mode = event["queryStringParameters"]["mode"]

    if mode == "upload":

        # Validate extension
        if "." not in file_name:
            return {
                "statusCode": 400,
                "headers": cors_headers(),
                "body": json.dumps(
                    {"error": "File name must have an extension (.jpg, .jpeg, .png)"}
                ),
            }

        ext = file_name.rsplit(".", 1)[-1].lower()

        if ext in ("jpg", "jpeg"):
            content_type = "image/jpeg"
        elif ext == "png":
            content_type = "image/png"
        else:
            return {
                "statusCode": 400,
                "headers": cors_headers(),
                "body": json.dumps({"error": "Only JPG, JPEG and PNG are allowed."}),
            }

        URL = s3.generate_presigned_post(Bucket=bucket_name, Key=file_name, Fields=None, Conditions=None, ExpiresIn=600)

    if mode == "download":

        URL = s3.generate_presigned_url("get_object", Params={"Bucket":bucket_name, "Key":f'bw-{file_name}'}, ExpiresIn=600)

    return {
            "statusCode": 200,
            "headers": cors_headers(),
            "body": json.dumps({"URL": URL}),
        }
