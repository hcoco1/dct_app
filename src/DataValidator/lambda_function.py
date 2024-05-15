import json
import boto3
import csv
import io
import os

def lambda_handler(event, context):
    """Processes an S3 event, separates records into 'processed' and 'error' CSVs, 
    and uploads them to respective S3 buckets.
    """
    
    # Initialize the s3 client using boto3.
    s3 = boto3.client('s3')
    
    # Define the name of the processed and error buckets in S3 
    # where you want to copy CSV data into.
    error_bucket = os.environ['ERROR_DCT_BUCKET']
    processed_bucket = os.environ['PROCESSED_DCT_BUCKET']
    # error_bucket = 'YOUR-HARDCODED-ERROR-BUCKET-NAME'
    # processed_bucket = 'YOUR-HARDCODED-PROCESSED-BUCKET-NAME'
    
    
    # Extract the 'bucket name' and the 'CSV filename' from 
    # the 'event' input and print the CSV filename
    raw_bucket = event['Records'][0]['s3']['bucket']['name']
    csv_filename = event['Records'][0]['s3']['object']['key']
    # print(f"\n{csv_filename}\n")
    
    # Download the CSV file from S3, read the content, decode from bytes to string, and split the content by lines
    obj = s3.get_object(Bucket=raw_bucket, Key=csv_filename)
    csv_data = obj['Body'].read().decode('utf-8').splitlines()
    # print(f"\n{csv_data}\n")
    
    # Create two empty lists which will store processed rows and error rows that will be extracted from the CSV data.
    processed_rows = []
    error_rows = []
    
    # 1. Create a For Loop that reads the CSV content line by line using Python's csv DictReader.
    #    reader = csv.DictReader(csv_data)
    # 2. Within the loop create an if condition that flags data with a missing price value and appends it to the 'error_rows' list.
    #    Else, append it to the processed_rows list.
    reader = csv.DictReader(csv_data)    
    for row in reader:        
        # print(row)
        # break
        if not row['price']:
            error_rows.append(row)
        else:    
            processed_rows.append(row)
    
    # print(error_rows)        
    # If the 'processed_rows' and 'error_rows' lists are populated pass them to the 'upload_to_bucket' function.
    if processed_rows:
        upload_to_bucket(s3, processed_bucket, processed_rows, csv_filename)
        
    if error_rows:
        upload_to_bucket(s3, error_bucket, error_rows, csv_filename)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
def upload_to_bucket(s3_client, bucket_name, upload_list, csv_filename):
    """Uploads a CSV file created from a list of dictionaries to a specified S3 bucket."""
    field_names = list(upload_list[0].keys())
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, field_names)
    writer.writeheader()
    writer.writerows(upload_list)
    csv_content = csv_buffer.getvalue()
        
    response = s3_client.put_object(Bucket=bucket_name, Key=csv_filename, Body=csv_content)
    print(response)