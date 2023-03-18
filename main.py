from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json
import os
from typing import Any, Optional
import openai

app = Flask(__name__)


def chat_gpt_request(prompt: Any) -> Optional[Any]:
    openai.api_key = os.environ['API_KEY']
    engine = "text-davinci-002"
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text


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