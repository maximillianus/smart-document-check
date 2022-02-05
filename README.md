# Smart Document Check
This is an API to identify PII document using Textract. This API is deployed through API Gateway and Lambda function which calls Textract endpoint.  
  
  <br>

# Steps to deploy API
1. Create lambda execution roles allowing access to Textract
2. Create a lambda function using `lambda_process_doc.py` code
3. Create and deploy API Gateway resource using AWS CDK in `cdk/` dir.
4. Upload identity documents and start getting result
  
  <br>
  
# AWS CDK
AWS CDK is a framework for defining cloud infrastructure in code and provisioning it through AWS CloudFormation [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html). To get started with AWS CDK, you can refer to this [CDK documentation] (https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html)

## Steps to install AWS CDK
1. Have AWS CLI installed and configure it with AWS credentials and AWS region
2. AWS CDK requires Typescript so install Typescript: `npm -g install typescript`
3. Install AWS CDK library: `npm -g install aws-cdk`
  
  <br>  

# Todo
1. Create an image saving to S3 process
2. ~~Create a CDK to deploy API Gateway Resource~~
3. Create Lambda CDK to deploy Lambda Resource
