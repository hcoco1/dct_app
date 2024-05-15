from aws_cdk import (
    Duration,
    Stack,
    aws_s3 as s3,
    aws_s3_notifications as s3_notif,
    RemovalPolicy as rp,
    aws_lambda
)
from constructs import Construct

class DctAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3
        raw_bucket = s3.Bucket.from_bucket_name(self, 'imported_bucket', 'YOUR-RAW-BUCKET-NAME')
        
        buckets = {
            'processed_dct': None,
            'error_dct': None
        }
        
        for id in buckets:
            buckets[id] = self.create_bucket(id)
        
        # LAMBDA    
        lambda_dv = aws_lambda.Function(self, 'DataValidator',
            runtime=aws_lambda.Runtime.PYTHON_3_10,
            timeout=Duration.seconds(10),
            handler='lambda_function.lambda_handler',
            code=aws_lambda.Code.from_asset("src/DataValidator/")
        )
        
        # EVENTS & PERMISSIONS
        raw_bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3_notif.LambdaDestination(lambda_dv))
        raw_bucket.grant_read_write(lambda_dv)
        buckets['processed_dct'].grant_read_write(lambda_dv)
        buckets['error_dct'].grant_read_write(lambda_dv)
        
        # ENVIRONMENTAL VARS
        lambda_dv.add_environment('PROCESSED_DCT_BUCKET', buckets['processed_dct'].bucket_name)
        lambda_dv.add_environment('ERROR_DCT_BUCKET', buckets['error_dct'].bucket_name)
            
    def create_bucket(self, id):
        bucket = s3.Bucket(self, id,
            removal_policy=rp.DESTROY,
            auto_delete_objects=True
        )
        
        return bucket