from flask import Flask, jsonify, request
app = Flask(__name__)
from werkzeug.serving import run_simple

@app.route('/', methods=['POST'])
def hello_world():
    text = request.form.get('text')
    if text == "sup":
      res = {
        "response_type": "in_channel",
        "text": "Cool Kids Club"
      }
    else:
      res = {
        "response_type": "in_channel",
        "text": "Not so cool"
      }
    
    return jsonify(res)

if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, app, use_reloader=True)