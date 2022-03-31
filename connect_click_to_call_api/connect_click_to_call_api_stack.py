from aws_cdk import (

    aws_lambda,
    aws_iam,
    core as cdk,

)

from aws_cdk import core
from spa_deploy import SPADeploy


LAMBDA_CONFIG = dict (
    timeout=core.Duration.seconds(20),       
    memory_size=256,
    tracing= aws_lambda.Tracing.ACTIVE,
    runtime=aws_lambda.Runtime.PYTHON_3_8)


from api_cors.api_cors import api_cors_lambda


class ConnectClickToCallApiStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        contact_flow_id = cdk.CfnParameter(self, "contacFlowId", type="String", description="Id del contact Flow")
        connect_instance_id = cdk.CfnParameter(self, "instanceId", type="String", description="Id de la Instancia")
        source_phone_number = cdk.CfnParameter(self, "sourcePhoneNumber", type="String", description="Numero telefonico de Connect en formato E.164")


        BASE_ENV_VARIABLES =  dict (
            CONTACT_FLOW_ID = contact_flow_id.value_as_string,
            CONNECT_INSTANCE_ID = connect_instance_id.value_as_string,
            SOURCE_PHONE_NUMBER = source_phone_number.value_as_string
        )
        
        lambda_backend = aws_lambda.Function(
            self,"make_call" ,handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.asset("./lambdas/make_call"),**LAMBDA_CONFIG, 
            environment=BASE_ENV_VARIABLES)

        lambda_backend.add_to_role_policy(aws_iam.PolicyStatement(actions=["connect:*"],
                                               resources=["*"]))

        api = api_cors_lambda(self, "call_customer","connect", "call_customer", "GET", lambda_backend)



        #SPADeploy(self, 'S3ReactDeploy').create_basic_site(index_doc='index.html',
        #                                                     website_folder='website/build')

        SPADeploy(self, 'S3ReactDeploy').create_site_with_cloudfront(index_doc='index.html',
                                                             website_folder='website/build')
        