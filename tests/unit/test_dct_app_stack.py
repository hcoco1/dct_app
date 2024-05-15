import aws_cdk as core
import aws_cdk.assertions as assertions

from dct_app.dct_app_stack import DctAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in dct_app/dct_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DctAppStack(app, "dct-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
