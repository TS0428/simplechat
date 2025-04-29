# lambda/index.py
import json
import os
import urllib.request
import urllib.error
import re  # 正規表現モジュールをインポート
import boto3

# モデルID
FASTAPI_URL = "https://eba9-34-16-166-116.ngrok-free.app"
FASTAPI_BASE = os.environ.get("FASTAPI_URL")

def lambda_handler(event, context):
    try:
        raw_body = event.get("body") or ""
        body = json.loads(raw_body)
        message = ("message", "")
        # FAST APIを呼び出し
        payload = {
                "prompt": message
                }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
                FAST_BASE + "/generate",
                data = data
                headers = {"Content-Type": "application/json"}
                method = "POST"
                )
        with urllib.request.urlopen(req) as res:
            resp_text = res.read().decode()
            resp_json = json.loads(resp_text)
        
        # アシスタントの応答を取得
        assistant_response = resp_json.get("response", "")
        
        # アシスタントの応答を会話履歴に追加
        messages.append({
            "role": "assistant",
            "content": assistant_response
        })
        
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
                "success": True,
                "response": assistant_response
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
