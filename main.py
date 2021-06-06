from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from pony.orm import *
from pony.flask import Pony

from models import *


app = Flask(__name__)
Pony(app)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = User.get(username=username)
    if user.password == password:
        return user

@app.route("/messages/", methods=["GET", "POST"])
@auth.login_required
def messages():
    if request.method == "POST":
        sender = auth.current_user()
        reciever = request.json['reciever']
        message = request.json['message']
        subject = request.json['subject']
        
        message_object = Message(
            sender=sender, reciever=reciever,
            message=message, subject=subject)

        return f"Message sent!"

    elif request.method == "GET":
        user = auth.current_user()
        which_messages = request.values.get('filter', 'all')
        if which_messages == 'all': 
            messages = select(
                m for m in Message if m.sender.id == user.id
                or m.reciever.id == user.id)
        else:
            read_status = which_messages == 'read'
            messages = select(
                m for m in Message if
                (m.sender.id == user.id or m.reciever.id == user.id)
                and (m.read == read_status))
        messages = [
            {
                'sender': message.sender.id,
                'reciever': message.reciever.id,
                'message': message.message,
                'subject': message.subject,
                'creation_date': str(message.creation_date),
                'read': message.read
            }
            for message in messages
        ]
        return make_response(jsonify(messages))

@app.route("/messages/<message_id>/",
                      methods=["GET", "DELETE"])
@auth.login_required
def message(message_id):
    message = Message[message_id]
    user = auth.current_user()
    if not (user == message.sender or user == message.reciever):
        return "Not allowed", 401
    if request.method == "GET":
        message = {
            'sender': message.sender.id,
            'reciever': message.reciever.id,
            'message': message.message,
            'subject': message.subject,
            'creation_date': str(message.creation_date),
            'read': message.read
        }
        return make_response(jsonify(message))
    elif request.method == "DELETE":
        message.delete()
        return "ok"

if __name__ == "__main__":
    app.run(debug=True)

