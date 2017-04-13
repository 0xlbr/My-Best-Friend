import logging
from dbm import library
from random import randint

import digest as digest
import requests
import hashlib
import quotes_scrape
import md5

from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

quotes = [
    "Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time.",
    "Only I can change my life. No one can do it for me.",
    "Life is 10% what happens to you and 90% how you react to it.",
    "Optimism is the faith that leads to achievement. Nothing can be done without hope and confidence."]


@ask.launch
def launch():
    return question("Welcome.").reprompt("I could tell you something about numbers if you ask me.")

@ask.intent('AMAZON.HelpIntent')
def help():
    return question("You can ask me to inspire you about specific topics").reprompt("Say, motivate me about work")


@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("I hope I was able to help you. Bye.")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return stop()


@ask.session_ended
def session_ended():
    return "", 200

@ask.intent('QuoteStreamIntent', mapping={"topic": "topic"})
def start_reading_quotes(topic):
    # fetch 20 random quotes (save strings)

    context = "<speak>"

    for i in range(0, len(quotes)-1):
        context = context + quotes[i] + "<break time=\"2s\" />"

    context = context + "</speak>"
    #session.attributes['timestamp_beginning'] = session.timestamp
    return statement(context)

@ask.intent('QuoteOneIntent', mapping={"topic": "topic"})
def tell_one_quote(topic):
    # save topic
    # fetch one random quote
    quote = quotes_scrape.get_quotes(topic)
    context = "<speak>" +  quote + "<break time=\"2s\" /> Would you like a new one? Or do you want to do something with this quote? </speak>"
    session.attributes['last_quote'] = quotes[0]

    return question(context)

@ask.intent('AuthorNameIntent')
def tell_name_of_author():
    # give the name of the author of the quote saved in the attributes of the session
    quote = session.attributes['last_quote'] 
    author = quotes_scrape.get_author(quote)
    context = "<speak>" +  author + "<break time=\"2s\" /> Would you like another quote? </speak>"
    return question(context)


@ask.intent('ShareQuoteIntent', mapping={'': ''})
def share_last_quote(time):
   # if session.attributes['current_quote'] != "":
    #    return statement("Sorry, I can't find the last quote.")
        #sharing string that's currently saved in session.attributes['current_quote']
    return statement("I successfully shared the quote.")


if __name__ == '__main__':
    app.run(debug=True)
