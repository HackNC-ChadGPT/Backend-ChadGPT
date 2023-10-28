from flask import Flask
import os

app = Flask(__name__)

@app.route('/getConfidence')
def hello_world():
    # call backend stuff
    return '42%'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9999))
    app.run(host='0.0.0.0', port=port)
