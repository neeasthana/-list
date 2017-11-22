import sys
import json
import simplenote
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse

# GLOBALS
list_separator = "\n\n\n\n"


with open('passwords.json', 'r') as passwords_file:
    passwords = json.load(passwords_file)

username = passwords["simplenote_username"]
password = passwords["simplenote_password"]


simplenote = simplenote.Simplenote(username, password)
"""
result = simplenote.get_note_list()

print(result)

print(simplenote.get_note("a31b6fa882c94c61ba53c52e0230798c")[0]["content"])
"""

app = Flask(__name__)

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



def format_list_name(list_name):
    list_name = list_name.strip()
    list_name = list_name.strip(":")
    list_name = list_name.replace(" ", "") #remove all whitespace
    list_name = list_name.replace("#", "") #replace all list beginnings
    list_name = list_name.upper()
    return list_name
    #TODO: add support for "/" or multi-named lists




def profile_lists(message_body):
    lists_split = message_body.split(list_separator)
    list_names = []
    for split in lists_split:
        list_name = split.split("\n")[0]
        list_name = format_list_name(list_name)
        list_names.append(list_name)
    return list_names



def add_keys_and_list_names():
    result = simplenote.get_note_list()
    with open('my_dict.json', 'w') as f:
        my_dict = {}
        for entry in result[0]:
            if entry["deleted"] == 0:
                note_id = entry["key"]
                message_body = simplenote.get_note(note_id)[0]["content"]
                list_names = profile_lists(message_body)

                tags = entry["tags"]
                if(entry and tags):
                    for tag in tags:
                        result_dict = {}
                        result_dict["list_id"] = note_id
                        result_dict["list_names"] = list_names
                        my_dict[tag.upper()] = result_dict
        print(my_dict)
        json.dump(my_dict, f)



def get_lists_from_tag(tag):
    tag = tag.upper()
    with open('my_dict.json', 'r') as data_file:
        data = json.load(data_file)
        if tag in data:
            return data[tag]
        else:
            raise Exception("Tag is not in database. Consider refreshing the database or supplying another list name")
            return None



def get_index_from_list_name(tag_entry, tag_name, list_name = None):
    if list_name is not None:
        list_name= list_name.upper()
    
    list_names = tag_entry["list_names"]
    
    if list_name is None:
        if tag_name in list_names:
            list_name = tag_name
        else:
            return 0
    if list_name in list_names:
        return list_names.index(list_name)
    else:
        raise Exception("List Name is not in database. Consider refreshing the database or supplying another list name")
        return None



def add_to_list(list_text, list_index, list_entry):
    lists_split = list_text.split(list_separator)
    target_list = lists_split[list_index]
    target_list = target_list + "\n- " + list_entry
    lists_split[list_index] = target_list
    lists_merge = list_separator.join(lists_split)
    return lists_merge



def process(message_body):
    # read tag name
    message_body = message_body.strip()
    message_split = message_body.split(" ")
    if message_split[0][0] is "@":
        tag = message_split[0][1:]
        message_body = " ".join(message_split[1:])

        lists_split = message_body.split("\n\n\n")
    else:
        raise Exception("Error. Message does not start with a list name")

    tag_entry = get_lists_from_tag(tag)

    if message_split[1][0] is "#":
        list_name = message_split[1][1:]
        message_body = " ".join(message_split[2:])
    else:
        list_name = tag

    # read list name TODO
    print(tag + " - " + list_name)
    list_index = get_index_from_list_name(tag_entry, list_name)
    #print(list_index)
    
    # get list
    list_object = simplenote.get_note(tag_entry["list_id"])
    list_text = list_object[0]["content"]

    # get coresponding list_id and list location
    updated_list = add_to_list(list_text, list_index, message_body)

    #list_object[0]["content"] = updated_list
    result = {"key":tag_entry["list_id"], "content":updated_list}

    #print(result)

    #print(simplenote.update_note(result))
    #print(simplenote.get_note(tag_entry["list_id"])[0]["content"])
    # insert text entry in correct location
    # update list with message
 
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=8080)
