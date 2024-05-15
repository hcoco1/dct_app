class DctAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Task 1:
        # - Examine 'properties.csv' file's header line (line 1) to choose a unique partition key.
        #   Reference: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html
        # Task 2:
        # - Determine the value we should pass to the 'type' parameter for the partition_key & sort_key.
        #   Remember DynamoDB supports types like STRING, NUMBER, and BINARY.
        table = dynamodb.Table(self, 'PropertiesTable',
            partition_key=dynamodb.Attribute(
                name=<'...'>,
                type=<...>
            ),
            sort_key=dynamodb.Attribute(
                name='creationDate',
                type=<...>
            ),
            removal_policy=RemovalPolicy.DESTROY,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
        
        # LAMBDA   
        lambda_dv = create_lambda()
        
        # Task 3:
        # - Grant 'write' permissions to the 'lambda_dv' lambda function on the DynamoDB table.
        #   HINT: Check the 'Methods' section of the reference doc linked above.
        