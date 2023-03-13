from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct

class FusionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        FusionAlertsDev = _lambda.Function(
            self, 'Fusion-getAlertServiceAPI-dev',
            description='Test Lambda Function for Fusion backend',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('Fusion-getAlertServiceAPI-dev'),
            handler="lambda_function.handler1,alerts.handler2,config.handler3",
        )

        FusionCasesDev = _lambda.Function(
            self, 'Fusion-getCaseServiceAPI-dev',
            description='Test Lambda Function for Fusion backend',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('Fusion-getCaseServiceAPI-dev'),
            handler="lambda_function.handler1,CaseDetails.handler2,cases.handler3,responseconfig.handler4",
        )

        FusionEventsDev = _lambda.Function(
            self, 'Fusion-getEventAPI-dev',
            description='Test Lambda Function for Fusion backend',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('Fusion-getEventAPI-dev'),
            handler="lambda_function.handler1,events.handler2",
        )

        FusionExportDev = _lambda.Function(
            self, 'Fusion-getExportData-dev',
            description='Test Lambda Function for Fusion backend',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('Fusion-getExportData-dev'),
            handler="lambda_function.handler1,config.handler2,exportData.handler3",
        )

        FusionSummaryDev = _lambda.Function(
            self, 'Fusion-getSummaryData-dev',
            description='Test Lambda Function for Fusion backend',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('Fusion-getSummaryData-dev'),
            handler="lambda_function.handler1,config.handler2,summaryData.handler3",
        )

        FusionOptionsDev = _lambda.Function(
            self, 'Fusion-optionsAPI-dev',
            description='Test Lambda Function for Fusion backend',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('Fusion-optionsAPI-dev'),
            handler="lambda_function.handler",
        )

        api = apigateway.RestApi(
            self,
            'fusion-test-backend-api',
            description='Test API for Fusion backend',
            deploy_options={
                 'stage_name': 'dev',
            }
        )

        alerts = api.root.add_resource("alerts")
        proxy = alerts.add_proxy(any_method=False)
        proxy.add_method("GET", apigateway.LambdaIntegration(FusionAlertsDev))
        proxy.add_method("OPTIONS", apigateway.LambdaIntegration(FusionOptionsDev))


        cases = api.root.add_resource("cases")
        proxy = cases.add_proxy(any_method=False)
        proxy.add_method("GET", apigateway.LambdaIntegration(FusionCasesDev))
        proxy.add_method("OPTIONS", apigateway.LambdaIntegration(FusionOptionsDev))


        events = api.root.add_resource("events")
        proxy = events.add_proxy(any_method=False)
        proxy.add_method("GET", apigateway.LambdaIntegration(FusionEventsDev))
        proxy.add_method("OPTIONS", apigateway.LambdaIntegration(FusionOptionsDev))

        export = api.root.add_resource("export")
        export.add_method("GET", apigateway.LambdaIntegration(FusionExportDev))
        export.add_method("OPTIONS", apigateway.LambdaIntegration(FusionOptionsDev))

        getSummaryData = api.root.add_resource("getSummaryData")
        getSummaryData.add_method("GET", apigateway.LambdaIntegration(FusionSummaryDev))
        getSummaryData.add_method("OPTIONS", apigateway.LambdaIntegration(FusionOptionsDev))


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
