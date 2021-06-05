from datetime import datetime
from pony.orm import *


db = Database()

class User(db.Entity):
    username = Required(str) # should be unique=True
    password = Required(str)
    sent_messages = Set('Message', reverse='sender')
    recieved_messages = Set('Message', reverse='reciever')

class Message(db.Entity):
    sender = Required(User, reverse='sent_messages')
    reciever = Required(User, reverse='recieved_messages')
    message = Optional(str)
    subject = Optional(str)
    creation_date = Required(datetime, default=datetime.now)
    read = Required(bool, default=False)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
