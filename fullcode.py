import boto3, json, os

bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="us-east-2")
KB_ID = "ZXGIU1GREJ"
MODEL_ARN = "arn:aws:bedrock:us-east-2::foundation-model/amazon.nova-micro-v1"  # adjust if needed

CORS_HEADERS = {
    "Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN", "*"),  # set to your S3 site in prod
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

def lambda_handler(event, context):
    # Preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {"statusCode": 204, "headers": CORS_HEADERS, "body": ""}

    try:
        body = event.get("body") or "{}"
        if isinstance(body, str):
            body = json.loads(body)
        user_question = body.get("message") or body.get("question") or "What is Continuous Delivery?"

        resp = bedrock_agent.retrieve_and_generate(
            input={"text": user_question},
            retrieveAndGenerateConfiguration={
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KB_ID,
                    "modelArn": MODEL_ARN
                },
                "type": "KNOWLEDGE_BASE"
            }
        )
        answer = resp["output"]["text"]

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({"response": answer})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(e)})
        }
