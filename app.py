from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        api_key = data.get('api_key')
        messages = data.get('messages')
        system = data.get('system')
        
        if not api_key:
            return jsonify({'error': 'API key is required'}), 400
        
        if not messages:
            return jsonify({'error': 'Messages are required'}), 400
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key,
        }
        
        payload = {
            'model': 'claude-sonnet-4-20250514',
            'max_tokens': 1024,
            'system': system,
            'messages': messages
        }
        
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            return jsonify({'error': response.text}), response.status_code
        
        data = response.json()
        return jsonify({
            'content': [{'text': data['content'][0]['text']}]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=False)
