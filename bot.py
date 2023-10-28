from flask import Flask, request, jsonify
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/getConfidence', methods=['POST'])
@cross_origin()
def hello_world():
    # call backend stuff
    try:
        data = request.json
        prompt = data.get('prompt')
        if prompt is not None:
            return jsonify({"result": "42.5%"})
        else:
            return jsonify({"error": "No 'prompt' data found in the request body"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9999))
    app.run(host='0.0.0.0', port=port)
