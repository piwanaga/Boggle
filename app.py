# import sys
# sys.path.append('/c/Users/phillip/Desktop/Springboard/VSCODE/Flask/19.5 Flask Testing/Boggle Exercise')

from boggle import Boggle
from flask import Flask, render_template, session, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config["SECRET_KEY"] = "HOTDOG"
debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def show_home():
    '''
    Calls the make_board method from Boggle class to create the game board and renders the home.html template with some variables passed in
    '''

    board = Boggle.make_board(boggle_game)
    session['board'] = board
    high_score = session.get('high_score', 0)
    game_count = session.get('game_count', 0)
    
    return render_template('home.html', board=board, high_score=high_score, game_count=game_count)

@app.route('/word-check', methods=['POST'])
def check_word():
    '''
    Checks the submitted word by calling check_valid_word from Boggle class and returns response
    '''

    word = request.form['word']
    response = Boggle.check_valid_word(boggle_game, session['board'], word)
    return jsonify(result=response)

@app.route('/store-data', methods=['POST'])
def store_data():
    '''
    Accepts the score for the completed game and checks if it is higher than the existing high score. If it is, it becomes the new high score and is stored in session. 

    Number of games played is incremented by 1 and stored in session.
    '''

    new_score = int(request.form['score'])
    high_score = session.get('high_score', 0)
    game_count = session.get('game_count', 0)

    game_count += 1
    if new_score > high_score:
        high_score = new_score
    
    session['game_count'] = game_count
    session['high_score'] = high_score
    return jsonify(high_score=high_score, game_count=game_count)
