# Import necessary modules
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
    table = os.environ['PROPERTIES_TABLE_NAME'] 
    
    # Uncomment these lines if you want to hardcode bucket names and table name
    # error_bucket = 'dctappstack-errordct1f23a858-i9ubop8rjzd4'
    # processed_bucket = 'dctappstack-processeddcteb7f6096-5rgxvawrs9jv'
    # table = 'DctAppStack-PropertiesTable324F3970-NEBNY78RCM74'
    
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
    required_keys = ['zpid', 'creationDate', 'unit', 'bedrooms', 
                    'bathrooms', 'homeType', 'priceChange', 'zipcode', 'city', 
                    'state', 'country', 'livingArea', 'taxAssessedValue', 
                    'priceReduction', 'datePriceChanged', 'homeStatus', 'price']
    
    # 1. Create a For Loop that reads the CSV content line by line using Python's csv DictReader.
    #    reader = csv.DictReader(csv_data)
    # 2. Within the loop create an if condition that flags data with a missing price value and appends it to the 'error_rows' list.
    #    Else, append it to the processed_rows list.
    reader = csv.DictReader(csv_data)    
    for row in reader:        
        try:
            # Check if 'price' field is missing or empty, and if so, raise a ValueError
            if 'price' not in row or not row['price']:
                raise ValueError("Missing price.")
            
            # Check if the price is a negative value, and if so, raise a ValueError
            price = int(row['price'])
            if price < 0:
                raise ValueError("Negative price.")
                
            # Create a dictionary containing only the required keys
            filtered_row = {}
            for key in required_keys:
                if key in row:
                    filtered_row[key] = row[key]
                
            # Append the filtered row to the processed_rows list
            processed_rows.append(filtered_row)
        except ValueError as ve:
            # Print error message and append the row to the error_rows list
            print(f"Error: {ve} for row item: {row}.")
            error_rows.append(row)
    
    # Print the processed and error rows for debugging
    # print(processed_rows)
    # print(error_rows)
    
    # If the 'processed_rows' and 'error_rows' lists are populated pass them to the 'upload_to_bucket' function.
    if processed_rows:
        upload_to_bucket(s3, processed_bucket, processed_rows, csv_filename)
        upload_to_dynamodb(table, processed_rows)
        
    if error_rows:
        upload_to_bucket(s3, error_bucket, error_rows, csv_filename)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def upload_to_dynamodb(table_name, items):
    """Uploads a list of items to the specified DynamoDB table."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    # Use batch_writer to write multiple items in a batch
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)
    
def upload_to_bucket(s3_client, bucket_name, upload_list, csv_filename):
    """Uploads a CSV file created from a list of dictionaries to a specified S3 bucket."""
    field_names = list(upload_list[0].keys())  # Get the field names from the first dictionary in the list
    csv_buffer = io.StringIO()  # Create an in-memory string buffer
    writer = csv.DictWriter(csv_buffer, field_names)  # Create a CSV writer
    writer.writeheader()  # Write the header row
    writer.writerows(upload_list)  # Write the data rows
    csv_content = csv_buffer.getvalue()  # Get the CSV content as a string
        
    # Upload the CSV content to the specified S3 bucket
    response = s3_client.put_object(Bucket=bucket_name, Key=csv_filename, Body=csv_content)
    print(response)  # Print the response from S3
