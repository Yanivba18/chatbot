import requests
import json
from bottle import request, response
from MyHTMLParser import MyHTMLParser
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

CURSES = [
    "fuck",
    "shit",
    "suck",
    "piss",
    "puss",
    "pussy",
    "dick",
    "cunt",
    "wanker",
    "d1ck",
    "bastard",
]


JOKES_API_BASE_URL = "https://sv443.net/jokeapi/category/Any"
my_bot = ChatBot(name='boto', read_only=True,
                 logic_adapters=['chatterbot.logic.BestMatch'])

small_talk = ['hi there!',
              'hi!',
              'how do you do?',
              'how are you?',
              'I\'m cool.',
              'fine, you?',
              'always cool.',
              'I\'m ok',
              'glad to hear that.',
              'I\'m fine',
              'glad to hear that.',
              'i feel awesome',
              'excellent, glad to hear that.',
              'not so good',
              'sorry to hear that.',
              'what\'s your name?',
              'I\'m boto. What\'s up?.']

# list_trainer = ListTrainer(my_bot)
# list_trainer.train(small_talk)

corpus_trainer = ChatterBotCorpusTrainer(my_bot)
corpus_trainer.train('chatterbot.corpus.english')


def check_user_response(msg):
    msg_lower_case = msg.lower()
    if not request.get_cookie("username"):
        print(">>>>>first if: ", request.get_cookie(
            "username"), ">>>>", request.cookies.username)
        response.set_cookie("username", "Guest")
        return construct_response("dancing", "Hi, my name is Boto. What is your name?")

    elif "my" in msg_lower_case and "name" in msg_lower_case:
        print(">>>>> second if")
        name = msg.split()[-1]
        response.set_cookie("username", name)
        # username = request.cookies.username
        return construct_response("excited", f"Hello {name}, nice to meet you. I'll remember your name now!")

    elif "__first*" in msg:
        print(">>>> third if")
        username = request.cookies.username
        return construct_response("excited", f"Welcome back {username}, if you want to know  what to ask, type 'help'")

    if did_user_curse(msg_lower_case):
        return did_user_curse(msg_lower_case)

    elif msg_lower_case == "help":
        return show_help()

    elif "joke" in msg_lower_case:
        return get_joke()

    elif "distance" in msg_lower_case and "between" in msg_lower_case and "and" in msg_lower_case:
        print(">>>>>>> in distance")
        distance, unused = get_distance(msg_lower_case)
        return construct_response("takeoff", distance)

    elif "directions" in msg_lower_case and "from" in msg_lower_case and "to" in msg_lower_case:
        return get_directions(msg_lower_case)

    # elif msg_lower_case.endswith("?"):
    #     return handle_question(msg_lower_case)

    else:
        print(">>>>>>>> else statement")
        bot_response = my_bot.get_response(msg_lower_case)
        print(bot_response)
        return construct_response("confused", str(bot_response))
        # return construct_response("confused", "I did not understand that, sorry. Try rephrasing or asking for help by typing 'help'.")


def did_user_curse(msg):
    split_msg = msg.split(" ")
    if any(word in CURSES for word in split_msg):
        return construct_response("crying", "This is not nice! I will not tolerate such language.")
    else:
        return False


def get_distance(msg):
    split_msg = msg.split(" ")
    fromIndex = int(split_msg.index("from")) + 1
    toIndex = int(split_msg.index("to"))

    params = {
        "origin": "+".join(split_msg[fromIndex:toIndex]),
        "destination": "+".join(split_msg[toIndex+1:]),
        "key": "#GOOGLE_API_KEY_HERE"
    }

    GOOGLE_MAPS_BASE_URL = "https://maps.googleapis.com/maps/api/directions/json?"

    data = requests.get(url=GOOGLE_MAPS_BASE_URL, params=params).json()
    # >>>>>>>>>>>>>>>>>>
    legs = data['routes'][0]['legs']
    journey_directions = ""

    journey_directions += f"The distance to your destination is {legs[0]['distance']['text']}."
    journey_directions += f" The time it will take to your destination is {legs[0]['duration']['text']}. >>>>>>>>"
    print(journey_directions)
    return journey_directions, legs


def get_directions(msg):
    journey_directions, legs = get_distance(msg)
    journey_directions += create_journey_instructions(legs[0]['steps'])

    return construct_response("takeoff", journey_directions)


def create_journey_instructions(steps):
    parser = MyHTMLParser()  # HTML parser for directions API data
    instruct = ""
    for step in steps:
        parser.feed(step['html_instructions'])
        instruct += parser.get_data() + ">>>>>"
    print(instruct)
    return instruct


def handle_question(question):
    # if "weather" in question:
    #     get_weather()
    # else:
    return construct_response("confused", "I don't understand your question. Sorry.")


def get_weather():
    return construct_response("ok", "not implemented yet")


def get_joke():
    print(">>> Getting joke from api")
    return request_joke_from_api(JOKES_API_BASE_URL)


def show_help():
    msg = "Questions you can ask me: 1. 'tell me a joke'. 2. 'tell me the distance between New York and Washington'. 3. 'give me directions from Tel Aviv to Ramat Gan'. You can tell me your name like this: 'my name is Boto'"
    return construct_response("ok", msg)


def construct_response(animation, msg):
    return {"animation": animation, "msg": msg}


def request_joke_from_api(base_url, params=None):
    if params is None:
        response = requests.get(url=base_url)
        data = response.json()
        print(">>> received response ", data)
        print(data['type'])
        if data['type'] == "twopart":
            joke = data['setup'] + ' ' + data['delivery']
        else:
            joke = data['joke']
        return construct_response("laughing", joke)


def set_cookie():
    print("not implemented yet")
