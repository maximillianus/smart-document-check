# Smart Document Check
API to identify PII document using Textract

# Steps to deploy API
1. Create lambda execution roles allowing access to Textract
2. Create a lambda function using `lambda_process_doc.py` code
3. Create and deploy API Gateway resource to connect to Lambda function
4. Upload identity documents and start getting result

# Todo
1. Create an image saving to S3 process
2. Create a CDK to deploy API Gateway Resource
