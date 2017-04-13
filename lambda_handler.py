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




# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """


def on_launch(launch_request, session):
    return build_response({'topic': 'none', 'index': -1}, build_speechlet_response("Welcome.", "Welcome. How can I help you?", "If you want to be motivated, just ask me to tell you a quote.", False))

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


def handle_session_end_request():
    card_title = "Skill Ended"
    speech_output = "Okay. Bye"
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


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

    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def help():
    return build_response({}, build_speechlet_response("Help","You can ask me to inspire you about specific topics", "You could for example say: motivate me about work.", False))

def list_quotes(topic, session):
    quotes = quotes_scrape.get_quotes(topic)
    context = "<speak>"

    for quote in quotes:
        context = context + quote + "<break time=\"2s\" />"

    context = context + "</speak>"
    return build_speechlet_response("Quotes", context, "", True)

def tell_one_quote(topic, session):
    quotes = quotes_scrape.get_quotes(topic)
    index = session['attributes']['index'] + 1
    context = "<speak>" +  quotes[index] + "</speak>"
    session.attributes['last_quote'] = quotes[0]

    return build_speechlet_response({'topic'}, "Quote", quotes[0], "Would you like a new one? Or do you want to do something with this quote?", False)

def share_last_quote(time):
   # if session.attributes['current_quote'] != "":
    #    return statement("Sorry, I can't find the last quote.")
        #sharing string that's currently saved in session.attributes['current_quote']
    return build_speechlet_response("I successfully shared the quote.")