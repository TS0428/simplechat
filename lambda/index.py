# lambda/index.py
import json
import os
import urllib.request
import urllib.error
import re  # 正規表現モジュールをインポート
import boto3

# モデルID
FASTAPI_URL = "https://e94c-34-82-5-125.ngrok-free.app"

def lambda_handler(event, context):
    try:
        raw_body = event.get("body") or ""
        body = json.loads(raw_body)
        message = body["message"]
        # FAST APIを呼び出し
        payload = {
                "prompt": message,
                "max_new_tokens": 512,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True
                }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
                url = f"{FASTAPI_URL}/generate",
                data = data,
                headers = {"Content-Type": "application/json"},
                method = "POST"
                )
        with urllib.request.urlopen(req) as res:
            resp_text = res.read().decode()
            resp_json = json.loads(resp_text)
        
        
        # 成功レスポンスの返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "generated_text": resp_json.get("generated_text", ""),
                "response": resp_json.get("response_time", 0)
            })
        }
        
    except Exception as error:
        print("Error:", str(error))
        
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
