from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'ChadGPT/'))

from ChadGPT.controller.default_controller import DefaultController

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/getConfidence', methods=['POST'])
@cross_origin()
def get_confidence():
    print('request received')
    try:
        data = request.json
        prompt = data.get('prompt')
        if prompt is not None:
            result = DefaultController().run(prompt)
            return jsonify({"result": result})
        else:
            return jsonify({"error": "No 'prompt' data found in the request body"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9999))
    app.run(host='0.0.0.0', port=port)
