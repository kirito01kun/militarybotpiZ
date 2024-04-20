from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import nrf_sender

app = Flask(__name__, static_url_path='/static')

temp = None

def update_temp():
    global temp
    while True:
        temp = nrf_sender.MAX_TEMP


update_thread = threading.Thread(target=update_temp)
update_thread.daemon = True
update_thread.start()

@app.route('/')
def index():
    return render_template('index.html', temp=temp)

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

    nrf_sender.send_nrf(message)

    return 'Message Sent'

@app.route('/get_temperature')
def get_temperature():
    global temp
    # Return the current temperature as JSON
    return jsonify({'temperature': temp})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
