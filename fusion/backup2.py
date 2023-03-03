from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_stepfunctions as stepfunctions,
)


class FusionStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        my_lambda = _lambda.Function(
            self, 
            'FusionLambdaFunction',
            description='Deploying Lambda Function Infrastrcture',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='fusioncontroller.handler',
        )
        
        api = apigateway.LambdaRestApi(
            self,
            'FusionControllerRestAPI',
            handler=my_lambda,
            description='Deploying REST API Infrastrcture',
            deploy_options={
                 'stage_name': 'dev',
            }
        )

        api.root.add_method("GET", apigateway.LambdaIntegration(my_lambda))
        api.root.add_method("POST", apigateway.LambdaIntegration(my_lambda))
        api.root.add_method("PUT", apigateway.LambdaIntegration(my_lambda))
        api.root.add_method("HEAD", apigateway.LambdaIntegration(my_lambda))
        api.root.add_method("OPTIONS", apigateway.LambdaIntegration(my_lambda))
        api.root.add_method("PATCH", apigateway.LambdaIntegration(my_lambda))
        api.root.add_method("DELETE", apigateway.LambdaIntegration(my_lambda))

        api_key = api.add_api_key("ApiKey", api_key_name="ApiKey", value="1234567890abcdefghij")
