zip handler.zip handler.py constants.py
func_name=$1
aws lambda update-function-code \
    --function-name "${func_name}" \
    --zip-file fileb://handler.zip
aws lambda update-function-configuration \
    --function-name "${func_name}" \
    --handler handler.lambda_handler
