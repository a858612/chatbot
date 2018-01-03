import sys
#from pygraphviz import *
import telegram
from flask import Flask, request

from transitions import State
from transitions.extensions import GraphMachine as Machine

states = [
    'init_state',
    State(name = 'action_state'),
    { 'name': 'drama_state'},
    'all_state'
]
transitions = [
    {'trigger':'get_action','source':'init_state','dest':'action_state'},
    ['get_all', 'init_state', 'all_state'],
    ['get_drama', 'init_state', 'drama_state'],
    ['back_drama', 'drama_state', 'init_state'],
    ['back_all', 'all_state', 'init_state'],
    ['back_action', 'action_state', 'init_state']
]
class Game(object):
    def response_all(self):
        print('all\n')
    def response_drama(self):
        print('drama\n')
    def response_action(self):
        print('action\n')
movie_bot = Game()
machine = Machine( model = movie_bot, states = states, transitions = transitions
, initial = 'init_state', title = 'figure record')
print(movie_bot.state)
#machine.add_states(['blue','red'])# a list
#machine.add_transition('r_to_b','red','blue')
machine.on_enter_all_state('response_all')
machine.on_enter_action_state('response_action')
machine.on_enter_drama_state('response_drama')
#record.get_graph().draw('state_diagram.png',prog ='dot')
app = Flask(__name__)
bot = telegram.Bot(token='514582278:AAHOXBV2qmRe8U1vPx6Jqv-lGOwFIbC3C5Q')

def _set_webhook():
    status = bot.set_webhook('https://44fdccd9.ngrok.io/hook')
    if not status:
        print('Webhook setup failed')
        sys.exit(1)

@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        text = update.message.text
        if text == "drama" :
            movie_bot.trigger('get_drama')
            update.message.reply_text("1. The Mountain II\n2. The Chaos Class\n3. The Shawshank Redemption")
            movie_bot.trigger('back_drama')
        elif text == "action" :
            movie_bot.trigger('get_action')
            update.message.reply_text("1. The Dark Knight\n2. Star Wars: Episode V - The Empire Strikes Back\n3. Inception")
            movie_bot.trigger('back_action')
        elif text == "all" :
            movie_bot.trigger('get_all')
            update.message.reply_text("1. The Shawshank Redemption\n2. The Godfather\n3. The Godfather: Part II\n4.  The Dark Knight\n5.  12 Angry Men")
            movie_bot.trigger('back_all')
    return 'ok'

if __name__ == "__main__":
    _set_webhook()
    app.run()
