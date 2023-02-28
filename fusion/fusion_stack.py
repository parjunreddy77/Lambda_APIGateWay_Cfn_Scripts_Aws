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
            self, 'FusionLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='fusioncontroller.handler',
        )
        
        state_machine = stepfunctions.StateMachine(self, "MyStateMachine",
            state_machine_type=stepfunctions.StateMachineType.EXPRESS,
            definition=stepfunctions.Chain.start(stepfunctions.Pass(self, "Pass"))
        )

        api = apigateway.RestApi(self, "Api",
            rest_api_name="FusionControllerRestAPI"
        )

        api.root.add_method("GET", apigateway.StepFunctionsIntegration.start_execution(state_machine))
        api.root.add_method("POST", apigateway.StepFunctionsIntegration.start_execution(state_machine))

        api_key = api.add_api_key("ApiKey", api_key_name="ApiKey", value="1234567890abcdefghij")

        plan = api.add_usage_plan("UsagePlan",
            name="Test",
        )
