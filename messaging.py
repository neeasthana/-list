import sys
import json
import simplenote
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from simplenote_interface import SimplenoteInterface

# GLOBALS
list_separator = "\n\n\n\n"


with open('passwords.json', 'r') as passwords_file:
    passwords = json.load(passwords_file)

username = passwords["simplenote_username"]
password = passwords["simplenote_password"]


simplenote = simplenote.Simplenote(username, password)
s = SimplenoteInterface(False)
"""
result = simplenote.get_note_list()

print(result)

print(simplenote.get_note("a31b6fa882c94c61ba53c52e0230798c")[0]["content"])
"""

app = Flask(__name__)

@app.route('/alexa', methods=['POST'])
def alexa():
    """processing handle for alexa app"""
    number = request.form['tag_name']
    number = request.form['list_name']
    message_body = request.form['Body']



@app.route('/sms', methods=['POST'])
def sms():
    # Get message parameters - number and message
    number = request.form['From']
    message_body = request.form['Body']
    
    if check_for_refresh(message_body):
        return

    process(message_body)


    # Send response
    resp = MessagingResponse()
    resp.message("Added to the list")
    #print('Hello {}, you said: {}'.format(number, message_body))
    return str(resp)



def check_for_refresh(message_body):
    if message_body.strip().upper() is "REFRESH":
        add_keys_and_list_names()
        return True
    return False



def process(message_body):
    message_body = message_body.strip()
    message_split = message_body.split(" ")
    if message_split[0][0] is "@":
        tag = message_split[0][1:]
        message_body = " ".join(message_split[1:])
    else:
        raise Exception("Error. Message does not start with a list name")

    tag_entry = s.get_lists_from_tag(tag)

    if message_split[1][0] is "#":
        list_name = message_split[1][1:]
        message_body = " ".join(message_split[2:])
    else:
        list_name = tag

    # read list name TODO
    list_index = s.get_index_from_list_name(tag_entry, tag, list_name)
    print(tag + " - " + list_name + " - " + str(list_index))
    #print(list_index)
    
    # get list
    list_object = simplenote.get_note(tag_entry["list_id"])
    list_text = list_object[0]["content"]

    # get coresponding list_id and list location
    updated_list_text = s.add_to_list(list_text, list_index, message_body)
    #result = {"key":tag_entry["list_id"], "content":updated_list}
    s.update_list(tag_entry["list_id"], updated_list_text)


 
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=8080)
