import boto3
import json

bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="us-east-2")

KNOWLEDGE_BASE_ID = "ZXGIU1GREJ"

def lambda_handler(event, context):
    user_question = event.get("question", "What is Continuous Delivery?")

    try:
        resp = bedrock_agent.retrieve_and_generate(
            input={"text": user_question},
            retrieveAndGenerateConfiguration={
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                    "modelArn": "arn:aws:bedrock:us-east-2::foundation-model/meta.llama3-3-70b-instruct-v1:0"
                },
                "type": "KNOWLEDGE_BASE"
            }
        )

        answer = resp["output"]["text"]

        return {
            "statusCode": 200,
            "body": json.dumps({"question": user_question, "answer": answer})
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
