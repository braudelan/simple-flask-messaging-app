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

db.bind(
    provider='postgres',
    user='sxptruajuhajbs',
    password='da91448e50910a8cb5dcba92a7d9425830a91f97b91d0a4905e82857fd457b38',
    host='ec2-52-45-179-101.compute-1.amazonaws.com',
    database='d5d9qt1gc2o21j')
db.generate_mapping(create_tables=True)
