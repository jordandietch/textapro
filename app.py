from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    response = MessagingResponse()
    message = Message()
    message.body('Hello World')
    response.append(message)
    return str(response)

if __name__ == "__main__":
    app.run()
