#!/usr/bin/env python3
import os

import aws_cdk as cdk

from dct_app.dct_app_stack import DctAppStack

env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
env_uswest = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='us-west-2')

app = cdk.App()

stack1 = DctAppStack(app, "DctAppStack", env=env)
stack2 = DctAppStack(app, "DctAppStack2", env=env_uswest)

app.synth()
