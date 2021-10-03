from flask import Flask,send_file
app = Flask(__name__)

@app.route('/', methods=['GET'])
def api_home():
    return send_file("index.html")

app.run(host='127.0.0.1', port=3002, threaded=False)