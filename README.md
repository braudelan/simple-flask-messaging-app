# simple-flask-messaging-app
### Send messages between users and retrieve exsisting messages.

---
* The app is hosted on [https://braudelan-messaging.herokuapp.com/](https://braudelan-messaging.herokuapp.com/)
* [link to postman collection](https://www.getpostman.com/collections/1e55cd395ddf4e1b245c)
* [examples.postman_collection.json](examples.postman_collection.json) contains examples of the different requests that can be made with the app.

## Rules
* Messages can only be sent by a logged-in user (authorized).
* Getting messegas, either by filtering or by specific message id, will only return messages associated with the logged-in user (as sender or as receiver).
* A message can only be deleted by its' sender or receiver.


