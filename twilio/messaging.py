import sys

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
 
    resp = twiml.Response()
    resp.message('Hello {}, you said: {}'.format(number, message_body))
    print('Hello {}, you said: {}'.format(number, message_body))
    return str(resp)
 
if __name__ == '__main__':
    app.run()
