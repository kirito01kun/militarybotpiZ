from flask import Flask, render_template, request
import subprocess
from nrf_sender import send_nrf

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message')
def send_message():
    direction = request.args.get('direction')

    # Map direction to the corresponding message
    messages = {
        'up': 'u',
        'down': 'd',
        'left': 'l',
        'right': 'r',
        'cup': 'cu',
        'cdown': 'cd'
    }

    message = messages.get(direction, 'Unknown Direction')

    send_nrf(message)
    return 'Message Sent'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
