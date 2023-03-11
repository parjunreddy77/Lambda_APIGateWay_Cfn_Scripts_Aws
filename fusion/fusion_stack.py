from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)

from constructs import Construct

class ArianaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_lambda = _lambda.Function(
            self, 'Fusion-getAlertServiceAPI-dev',
            description='Test Lambda Function for Fusion backend',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('sampledata/data'),
            handler='fusioncontroller.handler',
        )

        api = apigateway.LambdaRestApi(
            self,
            'fusion-test-backend-api',
            handler=my_lambda,
            proxy=False,
            description='Test API for Fusion backend',
            deploy_options={
                 'stage_name': 'dev',
            }
        )

        alerts = api.root.add_resource("alerts")
        proxy = alerts.add_proxy(any_method=False)
        proxy.add_method("GET", apigateway.LambdaIntegration(my_lambda))
        proxy.add_method("OPTIONS", apigateway.LambdaIntegration(my_lambda))

        cases = api.root.add_resource("cases")
        proxy = cases.add_proxy(any_method=False)
        proxy.add_method("GET", apigateway.LambdaIntegration(my_lambda))
        proxy.add_method("OPTIONS", apigateway.LambdaIntegration(my_lambda))

        events = api.root.add_resource("events")
        proxy = events.add_proxy(any_method=False)
        proxy.add_method("GET", apigateway.LambdaIntegration(my_lambda))
        proxy.add_method("OPTIONS", apigateway.LambdaIntegration(my_lambda))

        export = api.root.add_resource("export")
        export.add_method("GET", apigateway.LambdaIntegration(my_lambda))
        export.add_method("OPTIONS", apigateway.LambdaIntegration(my_lambda))

        getSummaryData = api.root.add_resource("getSummaryData")
        getSummaryData.add_method("GET", apigateway.LambdaIntegration(my_lambda))
        getSummaryData.add_method("OPTIONS", apigateway.LambdaIntegration(my_lambda))

        plan = api.add_usage_plan(
            'Fusion-API-Backend-Usage-Plan-dev',
            name='Fusion-API-Backend-Usage-Plan-dev',
            description='Adding a usage plan to validate API Key',
            throttle=apigateway.ThrottleSettings(
                rate_limit=100,
                burst_limit=500
            )
        )

        plan.add_api_stage(
            stage=api.deployment_stage,
            )

        api_key = api.add_api_key("fusion-api-key-dev", api_key_name="fusion-api-key-dev", value="1234567890abcdefghij", description="Adding API Key with Value")

        plan.add_api_key(api_key)
