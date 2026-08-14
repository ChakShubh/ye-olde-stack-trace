import json
import boto3

bedrock = boto3.client(service_name='bedrock-runtime')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        error_log = body.get('error', 'NullPointerException')
        mode = body.get('mode', 'pirate')
        
        if mode == 'medieval':
            prompt = f"""You are a 14th-century royal court bard. 
Translate this scary software error log into a dramatic, rhyming medieval ballad or court announcement.
Keep it creative, witty, and 3-5 sentences long.

Error Log:
{error_log}"""
        else:
            prompt = f"""You are a 17th-century pirate captain on the high seas. 
Translate this scary software error log into pirate naval terminology and sea-shanty lore.
Keep it creative, funny, and 3-5 sentences long. Ahoy!

Error Log:
{error_log}"""

        payload = {
            "messages": [{"role": "user", "content": [{"text": prompt}]}]
        }
        
        response = bedrock.invoke_model(
            modelId="amazon.nova-micro-v1:0",
            body=json.dumps(payload)
        )
        
        response_body = json.loads(response['body'].read())
        translated_text = response_body['output']['message']['content'][0]['text']
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'translation': translated_text})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
