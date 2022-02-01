import json
import urllib.parse
import boto3
import base64
from pprint import pprint

print('Loading function')

textractClient = boto3.client('textract')

def textract_process_s3(client, bucket, document):
    resp = {}
    try:
        resp = client.analyze_document(
            Document={'S3Object': {'Bucket': bucket, 'Name': document}},
            FeatureTypes=['FORMS']
            )
    except Exception as e:
        print('Error processing textract-s3')
        print('Error:', e)
        resp = {}
    return resp

def textract_process_docs(client, image):
    resp = {}
    try:
        resp = client.analyze_document(
            Document={'Bytes': base64.b64decode(image)},
            FeatureTypes=['FORMS']
            )
    except Exception as e:
        print('Error processing textract-s3')
        print('Error:', e)
        resp = {}
    return resp

def get_lines_from_textract(textract_resp):
    blocks = textract_resp['Blocks']
    linelist = []
    for item in blocks:
        if item['BlockType'] == 'LINE':
            # print(item['Text'])
            linelist.append(item['Text'])
    # print(linelist)
    return linelist

def get_words_from_textract(textract_resp):
    blocks = textract_resp['Blocks']
    wordlist = []
    for item in blocks:
        if item['BlockType'] == 'WORD':
            # print(item['Text'])
            wordlist.append(item['Text'])
    # print(wordlist)
    return wordlist

def parse_document(textract_resp):
    resp = {
        'doctype': 'unidentified', # Identity Card | Driver License | Unidentified
        'country': 'unidentified', # Indonesia | Malaysian | Thailand | Phillipines | Vietnam
        'given_name': 'unknown',
        'context': []
    }

    linelist = get_lines_from_textract(textract_resp)
    resp['context'] = linelist

    # Indonesian
    if 'NIK' in linelist or 'Provinsi' in linelist:
        resp['doctype'] = 'identity_card'
        resp['country'] = 'Indonesia'
        return resp
    
    if 'SURAT IZIN MENGEMUDI' in linelist or 'KEPOLISIAN NEGARA' in linelist:
        resp['doctype'] = 'driving_license'
        resp['country'] = 'Indonesia'
        return resp

    # Phillipines
    if 'Philippine Identification Card' in linelist:
        resp['doctype'] = 'identity_card'
        resp['country'] = 'Philippine'
        return resp

    if all(x in linelist for x in ['LAND TRANSPORTATION OFFICE', 'REPUBLIC OF THE PHILLIPINES']):
        resp['doctype'] = 'driving_license'
        resp['country'] = 'Philippine'
        return resp

    # Malaysian
    if 'MyKad' in linelist or 'KAD PENGENALAN MALAYSIA' in linelist or 'MALAYSIA' in linelist:
        resp['doctype'] = 'identity_card'
        resp['country'] = 'Malaysia'
        return resp

    if 'LESEN MEMANDU' in linelist or all(x in linelist for x in ['DRIVING LICENSE', 'MALAYSIA']):
        resp['doctype'] = 'driving_license'
        resp['country'] = 'Malaysia'
        return resp

    # Thailand
    if 'Thai' in linelist or 'Thai National ID Card' in linelist:
        resp['doctype'] = 'identity_card'
        resp['country'] = 'Thailand'
        return resp

    if all(x in linelist for x in ['DRIVING LICENSE', 'Kingdom of Thailand']):
        resp['doctype'] = 'driving_license'
        resp['country'] = 'Thailand'
        return resp

    # Vietnam
    if 'Socialist Republic of Vietnam' in linelist or 'Citizen Identity Card' in linelist:
        resp['doctype'] = 'identity_card'
        resp['country'] = 'Vietnam'
        return resp

    if all(x in linelist for x in ['DRIVER`S LICENSE', 'VIÊT NAM']):
        resp['doctype'] = 'driving_license'
        resp['country'] = 'Vietnam'
        return resp

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print(event)
    # file_content = base64.b64decode(event['content'])

    # Get the object from the event and show its content type
    # bucket = event['Records'][0]['s3']['bucket']['name']
    # print('Bucket:', bucket)
    
    # key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    # print('Object:', key)
    
    # response = textract_process_s3(textractClient, bucket, key)
    # parsed_resp = parse_document(response)

    # print(parsed_resp)
    imageBase64 = event['base64Image']
    print(type(imageBase64))
    resp = textract_process_docs(textractClient, imageBase64)

    parsed_resp = parse_document(resp)
    print(parsed_resp)

    
    return {
        'statusCode': 200,
        # 'body': json.dumps({
        #     'status_code': 200,
        #     'hello': 'lambda',
        #     'textract_response': parsed_resp
        # }),
        'body': {
            'status_code': 200,
            'hello': 'lambda',
            'textract_response': parsed_resp
        }
    }
    