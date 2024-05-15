def lambda_handler(event, context):
    ''' Entry point for your Lambda function. DataValidator Code'''
    
    '''Code that calls 'upload_to_dynamodb()'
       The code passes the 'table_name' and 
       a list of elements, 'items', that will be uploaded to DynamoDB.
    '''
    
def upload_to_dynamodb(table_name, items):
    # Task 1:
    # - Use boto3.resource() to create a DynamoDB service resource object.
    #   Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/index.html
    dynamodb = boto3.resource(<'...'>) # HINT: Check the 1st code snippet of the referenced doc above.
    
    # Task 2:
    # - Use the dynamodb resource to get a reference to an existing DynamoDB Table.
    #   Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#table
    table = dynamodb.Table(<...>) # HINT: Check the 2nd code snippet of the referenced doc above.
    
    # Task 3:
    # - Use the batch_writer to write multiple items to your DynamoDB table in batches.
    #   Inside the 'with' block, write a regular for-loop over each item in the 'items' list passed into the function.
    #   Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.batch_writer
    # - Hint: Use 'put_item' method of the batch writer to add each element from the items list. 
    #   Contrary to the snippet, no need to pass a dictionary with the 'HashKey', and 'Otherstuff' just pass the individual item.
    with table.batch_writer() as batch: 
        