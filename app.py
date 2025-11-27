from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
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
        
        client = anthropic.Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=1024,
            system=system,
            messages=messages
        )
        
        return jsonify({
            'content': [{'text': response.content[0].text}]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=False)
