from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



@app.route('/send-url', methods=['POST'])
def receive_url():
    data = request.get_json()
    url = data.get('url')
    
    # Do whatever processing you want with the URL
    # For example, print it
    print('Received URL:', url)
    
    response_data = {'message': 'URL received successfully'}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
