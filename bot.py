from flask import Flask, request, jsonify
import os
from flask_cors import CORS, cross_origin

import sys # TODO: Do packages properly
sys.path.append('./')
sys.path.append('./ChadGPT/controller/')
sys.path.append('./ChadGPT/jobs/')
sys.path.append('./ChadGPT/connectors/')
from ChadGPT.controller.default_controller import DefaultController

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
            result = DefaultController().run('What is the meaning of life?')
            return jsonify({"result": result})
        else:
            return jsonify({"error": "No 'prompt' data found in the request body"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9999))
    app.run(host='0.0.0.0', port=port)
