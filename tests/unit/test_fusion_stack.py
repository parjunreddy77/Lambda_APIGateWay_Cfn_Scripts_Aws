import aws_cdk as core
import aws_cdk.assertions as assertions

from fusion.fusion_stack import FusionStack

# example tests. To run these tests, uncomment this file along with the example
# resource in fusion/fusion_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = FusionStack(app, "fusion")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
