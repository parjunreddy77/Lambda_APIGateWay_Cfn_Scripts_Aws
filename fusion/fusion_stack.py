from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)


class FusionStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
      
        my_lambda = _lambda.Function(
            self, 'Fusion-getAlertServiceAPI-dev',
            description='Test Lambda Function for Fusion backend',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('sampledata'),
            handler='fusioncontroller.handler',
        )

        api = apigateway.LambdaRestApi(
            self,
            'fusion-test-backend-api',
            handler=my_lambda,
            description='Test API for Fusion backend',
            deploy_options={
                 'stage_name': 'dev',
            }
        )

        alerts = api.root.add_resource("alerts")
        alerts.add_method("GET", apigateway.LambdaIntegration(my_lambda))
        alerts.add_method("OPTIONS", apigateway.LambdaIntegration(my_lambda))

        cases = api.root.add_resource("cases")
        cases.add_method("GET", apigateway.LambdaIntegration(my_lambda))
        cases.add_method("OPTIONS", apigateway.LambdaIntegration(my_lambda))

        events = api.root.add_resource("events")
        events.add_method("GET", apigateway.LambdaIntegration(my_lambda))
        events.add_method("OPTIONS", apigateway.LambdaIntegration(my_lambda))

        export = api.root.add_resource("export")
        export.add_method("GET", apigateway.LambdaIntegration(my_lambda))
        export.add_method("OPTIONS", apigateway.LambdaIntegration(my_lambda))

        getsummarydata = api.root.add_resource("getsummarydata")
        getsummarydata.add_method("GET", apigateway.LambdaIntegration(my_lambda))
        getsummarydata.add_method("OPTIONS", apigateway.LambdaIntegration(my_lambda))

        test = api.root.add_resource("test")
        test.add_method("GET", apigateway.LambdaIntegration(my_lambda))
        test.add_method("OPTIONS", apigateway.LambdaIntegration(my_lambda))

        plan = api.add_usage_plan(
            'Fusion-API-Backend-Usage-Plan-dev',
            name='Fusion-API-Backend-Usage-Plan-dev',
            description='Adding usage plan for to validate API Key',
            throttle=apigateway.ThrottleSettings(
                rate_limit=100,
                burst_limit=500
            )
        )

        plan.add_api_stage(
            stage=api.deployment_stage,
            )

        api_key = api.add_api_key("fusion-api-key-dev", api_key_name="fusion-api-key-dev", value="1234567890abcdefghij")

        plan.add_api_key(api_key)        
