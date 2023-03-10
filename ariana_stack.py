from aws_cdk import (
    Stack,
    aws_apigateway as apigateway,
)

from constructs import Construct

class ArianaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

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
        proxy.add_method("GET")
