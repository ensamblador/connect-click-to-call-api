import os
import json
import boto3

client = boto3.client('connect')

CONTACT_FLOW_ID = os.environ.get('CONTACT_FLOW_ID')
CONNECT_INSTANCE_ID = os.environ.get('CONNECT_INSTANCE_ID')
SOURCE_PHONE_NUMBER = os.environ.get('SOURCE_PHONE_NUMBER')

def call_customer(params):
    TELEFONO = params['telefono']
    NOMBRE = params['nombre']
    
    try:
        response = client.start_outbound_voice_contact(
            DestinationPhoneNumber=TELEFONO,
            ContactFlowId=CONTACT_FLOW_ID,
            InstanceId=CONNECT_INSTANCE_ID,
            SourcePhoneNumber=SOURCE_PHONE_NUMBER,
            Attributes={
                'nombre': NOMBRE
            })
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return 'Te estamos llamando...a {}'.format(TELEFONO)
            
    except Exception as e:
        print (e)
        return "Error en la llamada"
            




def lambda_handler(event, context):
    
    print("se recibió:", event)

    qs_params = event['queryStringParameters']


    if (qs_params is not None) and ('nombre' in qs_params) and ('telefono' in qs_params):
        result = call_customer(qs_params)
        return build_response(200, result)

    
    else:
        return build_response(200, "Falta nombre y/o telefono (formato E.164)")





def build_response(status_code, json_content):
        return {
        'statusCode': status_code,
        "headers": {
            "Access-Control-Allow-Origin":"*",
			"Content-Type": "application/json",
			"Access-Control-Allow-Methods" : "GET, OPTIONS, POST, DELETE",
        },
        'body': json.dumps({'data':json_content})
    }
