from flask import Flask, jsonify, Response
import mimetypes
from multiprocessing import Queue
import threading
import flask.cli 
from flask_basicauth import BasicAuth   
flask.cli.show_server_banner = lambda *args: None
from config.mol import AUTH_USERNAME, AUTH_PSSSWD
import logging
logging.getLogger("werkzeug").disabled = True
import ctypes
import pyautogui



app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = AUTH_PSSSWD
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
lock_state = False
cq=Queue()


def queue_listener():
    global lock_state
    while True:
        
        # Block until an item is available in the queue
        if not cq.empty():
            item = cq.get()
            # Update lock state based on the item received
            #print(item)
            lock_state = not item['locked']


@basic_auth.required
@app.route('/lock')
def lock():
    ctypes.windll.user32.LockWorkStation()
    return jsonify({'locked': lock_state})


@basic_auth.required
@app.route('/get_lock_state')
def get_lock_state():
    global lock_state
    
    return jsonify({'locked': lock_state})



@basic_auth.required
@app.route('/<path:file_path>')
def hello(file_path):
    print(f'pages/{file_path}', 'rb')
    data = b''
    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = 'application/octet-stream'
    
    with open(f'pages/{file_path}', 'rb') as file:
        data = file.read()
    
    return Response(data, content_type=content_type)


@app.route('/media/playpause')
def play():
    pyautogui.press('playpause')
    #pyautogui.press("playpause")
    return jsonify({
        'success':True
    })
@app.route('/media/rewind')
def rewind():
    pyautogui.press("prevtrack")
    return jsonify({
        'success':True
    })

@app.route('/media/skip')
def skip():
    pyautogui.press("nexttrack")
    return jsonify({
        'success':True
    })



def run(queue):
    global cq
    cq=queue
    listener_thread = threading.Thread(target=queue_listener)
    listener_thread.daemon = True
    listener_thread.start()
    app.run(host='0.0.0.0', debug=False)

