import json

from flask import Flask, request, Response, json, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from pony.orm import *
from pony.flask import Pony

from models import *


app = Flask(__name__)
Pony(app)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = User.get(username=username) # could be nicer to return somthing 
    if user.password == password:
        return user



@app.route("/messages/", methods=["GET", "POST"])
@auth.login_required
def write_message():
    # import ipdb; ipdb.set_trace()
    if request.method == "POST":
        sender = auth.current_user()
        reciever = request.json['reciever']
        message = request.json['message']
        subject = request.json['subject']
        
        message_object = Message(sender=sender, reciever=reciever,
                             message=message, subject=subject)

        return f"Message sent! sender is {sender.username}"

    elif request.method == "GET":
        import os
        print("-----")
        print(os.environ)
        user = auth.current_user()
        which_messages = request.values.get('which', 'all')
        if which_messages == 'all': 
            messages = select(m for m in Message if m.sender.id == user.id or m.reciever.id == user.id) # filter on this variable

        else:
            messages = select(m for m in Message if (m.sender.id == user.id or m.reciever.id == user.id) and (m.read == (which_messages == 'read')) )
        messages = [{'sender': message.sender.id, 'reciever': message.reciever.id, 'message': message.message, 'subject': message.subject, 'creation_date': str(message.creation_date),  'read': message.read} for message in messages]
        return make_response(jsonify(messages))


@app.route("/messages/<message_id>/", methods=["GET", "DELETE"])
@auth.login_required
def message(message_id):
    message = Message[message_id]
    user = auth.current_user()
    if not (user == message.sender or user == message.reciever):
        return "not ok", 405
    if request.method == "GET":
        message = {'sender': message.sender.id, 'reciever': message.reciever.id, 'message': message.message, 'subject': message.subject, 'creation_date': str(message.creation_date),  'read': message.read}
        return make_response(jsonify(message))
    elif request.method == "DELETE":
        message.delete()
        return "ok"

if __name__ == "__main__":
    app.run(debug=True)

