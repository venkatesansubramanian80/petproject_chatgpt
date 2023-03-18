from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json
import os
from typing import Any, Optional

app = Flask(__name__)


def chat_gpt_request(prompt: Any) -> Optional[Any]:
    api_key: str = os.environ['API_KEY']
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "prompt": prompt,
        "max-tokens": 100,
        "n": 1,
        "stop": None,
        "temperature": 1.0,
    }

    response = requests.post("https://api.openai.com/v1/engines/davinci-codex/completions",
                             headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.form.get('Body', '').strip()
    response_msg = chat_gpt_request(incoming_msg)

    twiml = MessagingResponse()
    twiml.message(response_msg)
    return str(twiml)


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()