## Deploy:

zip -g package.zip lambda_function.py && aws lambda update-function-code --function-name get_stats --zip-file fileb://package.zip