#!/usr/bin/env python3
# This line indicates that the script should be run with the Python 3 interpreter

# Import necessary modules
import os

import aws_cdk as cdk  # AWS Cloud Development Kit

from dct_app.dct_app_stack import DctAppStack  # Import the DctAppStack class from the dct_app module

# Define the AWS environment using environment variables for the account and region
env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
# Uncomment the following line to define an environment specifically for the us-west-2 region
# env_uswest = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='us-west-2')

# Create an instance of the CDK application
app = cdk.App()

# Create an instance of the DctAppStack stack within the app, using the environment defined above
stack1 = DctAppStack(app, "DctAppStack", env=env)
# Uncomment the following line to create a second stack instance in the us-west-2 region
# stack2 = DctAppStack(app, "DctAppStack2", env=env_uswest)

# Synthesize the app, which prepares the app for deployment
app.synth()
