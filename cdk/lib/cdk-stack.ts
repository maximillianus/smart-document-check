import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';


export class CdkStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    const lambdaFunctionName = 'textract-upload-document'
    const importedLambda = lambda.Function.fromFunctionArn(
      this,
      lambdaFunctionName,
      `arn:aws:lambda:${Stack.of(this).region}:${Stack.of(this).account}:function:${lambdaFunctionName}`
    )
    // console.log('functionName', importedLambda.functionName)

    const api = new apigateway.RestApi(
      this,
      'smart-doc-api-cdk', {
      binaryMediaTypes: ['*/*'],
      description: 'Smart Document Analysis API using AWS CDKv2',
      deployOptions: {
        stageName: 'v1',
        // loggingLevel: apigateway.MethodLoggingLevel.INFO
      }
    });
    const identify = api.root.addResource('identify');

    const getLambdaIntegration = new apigateway.LambdaIntegration(
      importedLambda,
      {
        contentHandling: apigateway.ContentHandling.CONVERT_TO_TEXT,
        proxy: false,
        passthroughBehavior: apigateway.PassthroughBehavior.WHEN_NO_TEMPLATES,
        requestTemplates: {
          "image/png": '{\"base64Image\": \"$input.body\"}',
          "image/jpeg": '{\"base64Image\": \"$input.body\"}',
          'application/pdf': '{\"base64Image\": \"$input.body\"}',
        },
        integrationResponses: [
          {
            statusCode: '200',
            responseTemplates: {
              'application/json': ''
            }
          }
        ]
      }
    )

    identify.addMethod('PUT', getLambdaIntegration, {
      methodResponses: [
        { statusCode: '200' }
      ],
    });
  }
}
