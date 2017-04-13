"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------
import quotes_scrape
import boto3


def build_speechlet_response(title, output, content, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': "My Best Friend - " + title,
            'content': content
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




# --------------- Events ------------------

def on_session_started(session_started_request, session):
    return build_response({"topic": "none", "index": -1, "last_quote": "none"}, build_speechlet_response("Start", "<speak></speak>", "", "", False))


def on_launch(launch_request, session):
    return build_response({"topic": "none", "index": -1, "last_quote": "none"}, build_speechlet_response("Welcome.", "<speak>Welcome. I can give you a quote about whatever you want.</speak>", "", "If you want to be motivated, just ask me to tell you a quote.", False))

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


def handle_session_end_request():
    card_title = "Skill Ended"
    speech_output = "<speak>Okay. Bye</speak>"
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, "", None, should_end_session))


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])


    print(event)

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
        if event['request']['intent']['name'] == "QuoteStreamIntent":
            return list_quotes(event['request']['intent']['slots']['topic']['value'], event['session'])

        elif event['request']['intent']['name'] == "QuoteOneIntent":
            return tell_one_quote(event['request']['intent']['slots']['topic']['value'], event['session'])

        elif event['request']['intent']['name'] == "QuoteAnotherIntent":
            return tell_one_quote(event['session']['attributes']['topic'] , event['session'])

        elif event['request']['intent']['name'] == "ShareQuoteIntent":
            return send_to_email(event['session'])

        elif event['request']['intent']['name'] == "Stop":
            return build_response({}, build_speechlet_response("Closing", "<speak>Okay. Bye.</speak>", "", "", True))

    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


# --------------- Intents ------------------

def help():
    return build_response({}, build_speechlet_response("Help","<speak>You can ask me to inspire you about specific topics</speak>", "help", "You could for example say: motivate me about work.", False))

def list_quotes(topic, session):
    quotes = quotes_scrape.get_quotes(topic)
    context = '<speak> '
    app_content = ''

    for quote in quotes:
        context = context + quote + ' <break time=\"3s\"/> '
        app_content = app_content + "\n" + quote

    context = context + ' </speak>'

    return build_response({"topic": topic, "index": -1, "last_quote": "none"}, build_speechlet_response("Quotes", context, app_content, "", True))

def tell_one_quote(topic, session):
    quotes = quotes_scrape.get_quotes(topic)
    if (session['attributes'] == {}):
        index = 0
    else:
        index = session['attributes']['index'] + 1

    print(index)
    context = '<speak> ' + quotes[index] + ' </speak>'
    return build_response({"topic": topic, "index": index, "last_quote": quotes[index]}, build_speechlet_response("Quote", context, quotes[index], "Would you like a new one? Or do you want to do something with this quote?", False))


def todos_sns_topic():
    return boto3.resource('sns').Topic('arn:aws:sns:eu-west-1:847828999320:sharequote')


def send_to_email(session):
    message = session['attributes']['last_quote']
    todos_sns_topic().publish(Message=message, Subject="Here is the awesome quote")

    return build_response({"topic": session['attributes']['topic'], "index": session['attributes']['index'], "last_quote": session['attributes']['last_quote']}, build_speechlet_response("Success", "<speak>I successfully shared the quote.</speak>", "I successfully shared: " + session['attributes']['last_quote'], "I'm still here", False))