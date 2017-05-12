"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import random

# --------------- Helpers that build all of the responses ----------------


def build_response(session_attributes, title,
                   output, reprompt_text, should_end_session):
    response = {
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

    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': response
    }


# --------------- Functions that control the skill's behavior ------------

# TODO: get actual feed and id
def get_facebook_feed():
    new_feed = "Sung says Today is very good"
    new_feed_id = str(random.randint(1, 100))

    return new_feed, new_feed_id


def get_feed(session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    card_title = "New Feed"

    new_feed, new_feed_id = get_facebook_feed()

    session_attributes = {"facebook_feed_id": new_feed_id}
    session['attributes'] = session_attributes

    speech_output = "New feed: " + new_feed

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "What would you comment on it?"
    should_end_session = False
    return build_response(session_attributes, card_title, speech_output, reprompt_text, should_end_session)


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Facebook Gini!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, card_title, speech_output, None, should_end_session)


def add_comment(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    facebook_id = ""

    # Get facebook id from the session. No session? Error??
    if "facebook_feed_id" in session.get('attributes', {}):
        facebook_id = session['attributes']['facebook_feed_id']
        print("Facebook id:" + facebook_id)
    else:
        speech_output = "Something went wrong. No facebook post id!" \
                        "Please try again."
        should_end_session = True
        return build_response({}, card_title, speech_output, "", should_end_session)

    should_end_session = False

    if 'Comment' in intent['slots']:
        comment = intent['slots']['Comment']['value']
        speech_output = "I added \"" + comment + "\" on " + facebook_id
        print("Comment done:" + speech_output)

        # TODO: add the comment in the facebook
        reprompt_text = "Do you want next feed?"
    else:
        speech_output = "I'm not sure what you said" \
                        "Please try again."
        reprompt_text = "What would you comment on it?"

    return build_response(session_attributes,
                          card_title, speech_output, reprompt_text, should_end_session)

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
    return get_feed(session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "CommentIntent":
        return add_comment(intent, session)
    elif intent_name == "AMAZON.HelpIntent" or "AMAZON.YesIntent":
        return get_feed(session)
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
