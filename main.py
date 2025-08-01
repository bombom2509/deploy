import os
import json
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
print("🔑 Using Together key:", TOGETHER_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://astonishing-panda-c4aba8.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7
    }

    # Debug logs
    print("=== Sending request to Together.ai ===")
    print("Headers:")
    print(json.dumps(headers, indent=2))
    print("Payload:")
    print(json.dumps(payload, indent=2))

    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers=headers,
            json=payload
        )
        print("Status code:", response.status_code)
        print("Response body:", response.text)
        response.raise_for_status()
        return {"response": response.json()["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
