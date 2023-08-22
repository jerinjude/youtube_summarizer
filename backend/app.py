from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def extract_title(url):
    return (url + '\n')* 500

@app.route('/send-url', methods=['POST'])
def receive_url():
    data = request.get_json()
    url = data.get('url')
    
    processed_url = extract_title(url)  # Call the extract_title function
    
    response_data = {'message': 'URL received successfully', 'processed_url': processed_url}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
