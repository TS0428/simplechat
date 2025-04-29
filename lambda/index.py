# lambda/index.py
import json
import os
import urllib.request
import urllib.error
import re  # 正規表現モジュールをインポート
import boto3

# Lambda コンテキストからリージョンを抽出する関数
def extract_region_from_arn(arn):
    # ARN 形式: arn:aws:lambda:region:account-id:function:function-name
    match = re.search('arn:aws:lambda:([^:]+):', arn)
    if match:
        return match.group(1)
    return "us-east-1"  # デフォルト値

# グローバル変数としてクライアントを初期化（初期値）
bedrock_client = None

# モデルID
FASTAPI_URL = "https://eba9-34-16-166-116.ngrok-free.app"
FASTAPI_BASE = os.environ.get("FASTAPI_URL")

def lambda_handler(event, context):
    try:
        messages = []
        messages.append({"role": "user", "content": message})
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
            resp = json.loads(res.read().decode())
        
        # アシスタントの応答を取得
        assistant_response = resp("response", "")
        
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
