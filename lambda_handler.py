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
import random


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

        elif event['request']['intent']['name'] == "AuthorIntent":
            return say_author_name(event['session'])

        elif event['request']['intent']['name'] == "AdviceIntent":
            return tell_one_advice(event['request']['intent']['slots']['topic']['value'], event['session'])

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
    if ('attributes' in session):
        if (session['attributes'] == {}): #or session['attributes'] == {}):
         index = 0
        else:
         index = session['attributes']['index'] + 1
    else:
        index = 0

    context = '<speak> ' + quotes[index] + ' </speak>'
    return build_response({"topic": topic, "index": index, "last_quote": quotes[index]}, build_speechlet_response("Quote", context, quotes[index], "Would you like a new one? Or do you want to do something with this quote?", False))

def tell_one_advice(topic, session):
    advice = {"study": [
                        "Remember that being well hydrated is essential for your brain to work at its best. Make sure you keep drinking plenty of water throughout your revision, and also on the exam day",
                        "Develop a study routine that works for you. If you study better in the morning, start early before taking a break at lunchtime. Or if you're more productive at nighttime, take a larger break earlier on so you're ready to settle down come evening.",
                        "Get together with friends for a study session. You may have questions that they have the answers to and vice versa. As long as you make sure you stay focused on the topic for an agreed amount of time, this can be one of the most effective ways to challenge yourself.",
                        "Give yourself enough time to study. Don't leave it until the last minute. While some students do seem to thrive on last-minute 'cramming', it's widely accepted that for most of us, this is not the best way to approach an exam.",
                        "Use flow charts and diagrams. Visual aids can be really helpful when revising. At the start of a topic, challenge yourself to write down everything you already know about a topic - and then highlight where the gaps lie.",
                        "Try and get rid of all distractions, and make sure you feel as comfortable and able to focus as possible. For some people, this may mean almost complete silence; for others, background music helps.",
                        ],
              "work": [
                        "Just as you need to let go of work to enjoy your time at home, it's important to leave personal worries at home so you can focus and be productive at work.",
                        "Carry a schedule and record all your thoughts, conversations and activities for a week. This will help you understand how much you can get done during the course of a day and where your precious moments are going. You'll see how much time is actually spent producing results and how much time is wasted on unproductive thoughts, conversations and actions.",
                        "Plan to spend at least 50 percent of your time engaged in the thoughts, activities and conversations that produce most of your results.",
                        "Take the first 30 minutes of every day to plan your day. Don't start your day until you complete your time plan. The most important time of your day is the time you schedule to schedule time.",
                        "Block out other distractions like Facebook and other forms of social media unless you use these tools to generate business.",
                        "Remember that it's impossible to get everything done. Also remember that odds are good that 20 percent of your thoughts, conversations and activities produce 80 percent of your results.",
                        ],
              "general": [
                        "Make the journey fun. It’s an awesome game! The minute you make it serious, there’s a big chance it will start carrying a heavy emotional weight and you will lose perspective and become stuck again.",
                        "Motivation means action and action brings results. Sometimes your actions fail to bring the results you want. So you prefer to be nice to yourself and not put yourself in a difficult situation.",
                        "Don’t rely on others. You should never expect others to do it for you, not even your partner, friend or boss. They are all busy with their own needs. No one will make you happy or achieve your goals for you. It’s all on you.",
                        "Plan. Know your three steps forward. You do not need more.",
                        "You have the opportunity to make a difference in the world and in yourself. Make the day meaningful.",
                        "Your thoughts become what you are. What you think, you believe.",
                        ],
    randomIndex = random.randint(0,5)
    if topic == "study":
        this_advice = advice["study"][randomIndex]
    elif topic == "work":
        this_advice = advice["work"][randomIndex]
    else:
        this_advice = advice["general"] [randomIndex]
    context = '<speak> ' + this_advice + ' </speak>'
    return build_response({"topic": topic, "last_quote": this_advice}, build_speechlet_response("Quote", context, this_advice, "Would you like a new one? Or do you want to share this advice?", False))


def say_author_name(session):
    quote = session['attributes']['last_quote']
    topic = session['attributes']['topic']
    author = quotes_scrape.get_author(topic, quote)
    return build_response({"topic": session['attributes']['topic'], "index": session['attributes']['index'], "last_quote": session['attributes']['last_quote']}, build_speechlet_response("Author", "<speak>" + author +  "</speak>", "The author of quote " + session['attributes']['last_quote'] + " is " + author, "I'm still here", False))

def todos_sns_topic():
    return boto3.resource('sns').Topic('arn:aws:sns:eu-west-1:847828999320:sharequote')


def send_to_email(session):
    message = session['attributes']['last_quote']
    todos_sns_topic().publish(Message=message, Subject="Here is the awesome quote")

    return build_response({"topic": session['attributes']['topic'], "index": session['attributes']['index'], "last_quote": session['attributes']['last_quote']}, build_speechlet_response("Success", "<speak>I successfully shared the quote.</speak>", "I successfully shared: " + session['attributes']['last_quote'], "I'm still here", False))
