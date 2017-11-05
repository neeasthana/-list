import sys

from flask import Flask, request, redirect
from twilio import twiml

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    
    print("got here")
    print(number, message_body)

    resp = twiml.Response()
    resp.message('Hello {}, you said: {}'.format(number, message_body))
    print('Hello {}, you said: {}'.format(number, message_body))
    return str(resp)
 
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=8080)
