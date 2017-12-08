"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import urllib
from urllib import request, parse


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = create_addition_counter()
    card_title = "Welcome"
    speech_output = "Welcome to at list. " \
                    "Please tell me what you would like to add to a list, " \
                    "or to read off the names of your lists"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what you would like to add to a list, " \
                    "or to read off the names of your lists"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using at list. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_addition_counter():
    return {"additions": 0}

def increment_addition_counter():
    return {"additions": 1}

def add_to_list(intent, session):
    """ Adds an item to a specified list
    """

    card_title = "Success"#intent['name']
    session_attributes = {}
    should_end_session = True

    if 'tag_name' in intent['slots']:
        tag_name = intent['slots']['tag_name']['value']

        if 'update_item' in intent['slots']:

            update_item = intent['slots']['update_item']['value']

            list_name = tag_name
            if 'list_name' in intent['slots']:
                list_name = intent['slots']['list_name']['value']

            populated_url = "http://34.201.91.109:8080/alexa"
            post_params = {"tag_name": tag_name, "list_name": list_name, "message_body": update_item}
         
            # encode the parameters for Python's urllib
            data = parse.urlencode(post_params).encode()
            req = request.Request(populated_url)
         
            # add authentication header to request based on Account SID + Auth Token
            # authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            # base64string = base64.b64encode(authentication.encode('utf-8'))
            # req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
         
            try:
                # perform HTTP POST request
                with request.urlopen(req, data) as f:
                    print("@List returned {}".format(str(f.read().decode('utf-8'))))
            except Exception as e:
                # something went wrong!
                return e


            session_attributes = increment_addition_counter()
            speech_output = "Okay. I added that to " + \
                            tag_name + \
                            ". You can ask me to do another addition to a list."
            reprompt_text = "You can ask me to do another addition to a list."
        else:
            speech_output = "I did not understand the item you wanted to add to " + \
                            tag_name + \
                            "Please try again."
            reprompt_text = "I did not understand the item you wanted to add to " + \
                            tag_name + \
                            "Please try again." + \
                            "You can tell me a tag name by saying, " + \
                            "add to a specific tag"
    else:
        speech_output = "I did not understand the tag name you used. " + \
                        "Please try again."
        reprompt_text = "I did not understand the tag name you used. " + \
                        "You can tell me a tag name by saying, " + \
                        "add to a specific tag"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_lists_from_tag(intent, session):
    session_attributes = {}
    reprompt_text = None

    if 'tag_name' in intent['slots']:
        tag_name = intent['slots']['tag_name']['value']

        populated_url = "http://34.201.91.109:8080/alexaListFromTag?tag_name="+tag_name
        # encode the parameters for Python's urllib
        req = request.Request(populated_url)
        try:
            # perform HTTP POST request
            with request.urlopen(req) as f:
                response = str(f.read().decode('utf-8'))
                print("@List returned {}".format(str(f.read().decode('utf-8'))))
                speech_output = "The lists included in the " + tag_name + " tag are " + response
                should_end_session = True
        except Exception as e:
            # something went wrong!
            return e
    else:
        speech_output = "I did not understand the tag name you used. " + \
                        "Please try again."
        reprompt_text = "I did not understand the tag name you used. " + \
                        "You can tell me a tag name by saying, " + \
                        "add to a specific tag"
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AddToAtListIntent":
        return add_to_list(intent, session)
    elif intent_name == "AddToAtTagListIntent":
        return add_to_list(intent, session)
    elif intent_name == "AllListsFromTagIntent":
        return get_lists_from_tag(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

if __name__ == '__main__':
    intent = {
        "slots": {
              "tag_name" : {"value":"phipsi"},
              #"update_item": {"value":"smash raj"},
              #"list_name": {"value":"nicknames"}
            }
        }
    #intent['slots']['tag_name']['value'] = "books"
    #intent['slots']['update_item']['value'] = "from many to one"
    print(intent)
    #add_to_list(intent, {})
    print(get_lists_from_tag(intent, {}))