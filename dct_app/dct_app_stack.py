# Import necessary modules from AWS CDK (Cloud Development Kit)
from aws_cdk import (
    Duration,  # Used to specify time durations
    Stack,  # Represents a CDK stack
    aws_s3 as s3,  # AWS S3 service
    aws_s3_notifications as s3_notif,  # S3 notifications for triggering events
    RemovalPolicy as rp,  # Defines policies for resource removal
    aws_lambda,  # AWS Lambda service
    aws_dynamodb as dynamodb  # AWS DynamoDB service
)
from constructs import Construct  # Construct class for defining reusable cloud components

# Define a stack class for the application
class DctAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        # Initialize the stack with scope and construct ID
        super().__init__(scope, construct_id, **kwargs)

        # S3: Import an existing S3 bucket by name
        raw_bucket = s3.Bucket.from_bucket_name(self, 'imported_bucket', 'python3-boto3-hcoco1-test-bucket')
        
        # Dictionary to store processed and error buckets
        buckets = {
            'processed_dct': None,
            'error_dct': None
        }
        
        # Create the processed and error buckets
        for id in buckets:
            buckets[id] = self.create_bucket(id)
        
        # LAMBDA: Create a Lambda function for data validation
        lambda_dv = aws_lambda.Function(self, 'DataValidator',
            runtime=aws_lambda.Runtime.PYTHON_3_10,  # Specify the runtime environment
            timeout=Duration.seconds(10),  # Set the timeout duration
            handler='lambda_function.lambda_handler',  # Specify the handler function
            code=aws_lambda.Code.from_asset("src/DataValidator/")  # Define the source code location
        )
        
        # DYNAMODB: Create a DynamoDB table
        table = dynamodb.Table(self, 'PropertiesTable',
            partition_key=dynamodb.Attribute(
                name='zpid',  # Define the partition key
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='creationDate',  # Define the sort key
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=rp.DESTROY,  # Set the removal policy to destroy
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST  # Set the billing mode to pay per request
        )
        
        # EVENTS & PERMISSIONS: Add S3 event notification and permissions
        raw_bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3_notif.LambdaDestination(lambda_dv))
        raw_bucket.grant_read_write(lambda_dv)  # Grant read/write permissions to the Lambda function
        buckets['processed_dct'].grant_read_write(lambda_dv)  # Grant read/write permissions to the processed bucket
        buckets['error_dct'].grant_read_write(lambda_dv)  # Grant read/write permissions to the error bucket
        table.grant_write_data(lambda_dv)  # Grant write permissions to the DynamoDB table
        
        # ENVIRONMENT VARIABLES: Add environment variables to the Lambda function
        lambda_dv.add_environment('PROCESSED_DCT_BUCKET', buckets['processed_dct'].bucket_name)
        lambda_dv.add_environment('ERROR_DCT_BUCKET', buckets['error_dct'].bucket_name)
        lambda_dv.add_environment('PROPERTIES_TABLE_NAME', table.table_name)
    
    # Method to create an S3 bucket
    def create_bucket(self, id):
        bucket = s3.Bucket(self, id,
            removal_policy=rp.DESTROY,  # Set the removal policy to destroy
            auto_delete_objects=True  # Automatically delete objects when the bucket is deleted
        )
        
        return bucket  # Return the created bucket
