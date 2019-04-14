import os

from bottle import Bottle, run, request, template

import ausmash_lib

app = Bottle()

@app.route('/')
def index():
	#I should use IDs...
	regions = {region['Short']: region['Name'] for region in ausmash_lib.get_regions()}
	games = {game['Short']: game['Name'] for game in ausmash_lib.get_games()}
	return template('main_form', regions=regions, games=games)

@app.route('/main')
def get_stuff():
	region = request.query.region
	player = request.query.player
	game = request.query.game
	scores = ausmash_lib.group_player_score_against_characters(region, player, game)
	return template('scores_view', region=region, player=player, game=game, scores=scores)

run(app, host='0.0.0.0', port=os.environ.get('PORT', 5000))