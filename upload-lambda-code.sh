zip handler.zip handler.py constants.py
func_name=$1
aws lambda update-function-code \
    --function-name "${func_name}" \
    --zip-file fileb://handler.zip