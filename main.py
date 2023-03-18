import requests
import json
import sseclient
import os

def performRequestWithStreaming():
    reqUrl = 'https://api.openai.com/v1/completions'
    api_key: str = os.environ['API_KEY']
    reqHeaders = {
        'Accept': 'text/event-stream',
        'Authorization': 'Bearer ' + api_key
    }
    reqBody = {
        "model": "text-davinci-003",
        "prompt": "what is the square root of 100",
        "max_tokens": 100,
        "temperature": 0,
        "stream": True,
    }
    request = requests.post(reqUrl, stream=True, headers=reqHeaders, json=reqBody)
    client = sseclient.SSEClient(request)
    for event in client.events():
        if event.data != '[DONE]':
            print(json.loads(event.data)['choices'][0]['text'], end="", flush=True),

