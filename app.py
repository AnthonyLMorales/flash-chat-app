from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

acc = {}
counter = 0


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/button')
def button():
    return render_template("button.html")


@socketio.on('load_counter')
def handle_load_count():
    socketio.emit('receive_counter', counter)


@socketio.on('button_click')
def handle_button_click():
    global counter
    print(counter)
    counter += 1
    socketio.emit('receive_counter', counter)


@app.route('/chat')
def chat():
    username = request.args.get('username')
    if username:
        return render_template('chat.html', username=username)
    else:
        return redirect("/")


@socketio.on('send_message')
def handle_sent_message_event(data):
    print(data)
    socketio.emit('receive_message', data)


if __name__ == "__main__":
    socketio.run(app, debug=True)
