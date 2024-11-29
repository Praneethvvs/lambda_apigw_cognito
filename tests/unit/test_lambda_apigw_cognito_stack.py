import aws_cdk as core
import aws_cdk.assertions as assertions

from lambda_apigw_cognito.lambda_apigw_cognito_stack import LambdaApigwCognitoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lambda_apigw_cognito/lambda_apigw_cognito_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LambdaApigwCognitoStack(app, "lambda-apigw-cognito")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
