import sys
import simplenote
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse

app = Flask(__name__)

username = "neeasthana@gmail.com"
password = "Waterbottle94"

@app.route('/sms', methods=['POST'])
def sms():
    # Get message parameters - number and message
    number = request.form['From']
    message_body = request.form['Body']
    
    # Establish connection to simplenote
    simplenote = simplenote.Simplenote(username, password)

    # Parse out list name using "@" annotation
    message_split = message_body.split(" ")
    if message_split[0][0] is "@":
        list_name = message_split[0][1:]
        message_body = message_split[1:].join(" ")
    else: 
        print("Error. Message does not start with a list name")

    # Send response
    resp = MessagingResponse()
    resp.message('Hello {}, you said: {}'.format(number, message_body))
    print('Hello {}, you said: {}'.format(number, message_body))
    return str(resp)
 
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=8080)
