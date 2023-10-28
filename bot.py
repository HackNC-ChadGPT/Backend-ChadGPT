from flask import Flask

app = Flask(__name__)

@app.route('/getConfidence')
def hello_world():
    # call backend stuff
    return '42%'

if __name__ == '__main__':
    app.run()
