import os
from urllib.request import HTTPError

from bottle import Bottle, run, request, template

import ausmash_lib

app = Bottle()

@app.route('/')
def index():
	return template('main_page')

@app.route('/character_matchups/main')
def character_matchups():
	#I should use IDs...
	regions = {region['Short']: region['Name'] for region in ausmash_lib.get_regions()}
	games = {game['Short']: game['Name'] for game in ausmash_lib.get_games()}
	return template('character_matchups_main', regions=regions, games=games)

@app.route('/character_matchups/results')
def character_matchup_results():
	region = request.query.region
	player = request.query.player
	game = request.query.game
	
	try:
		player_id = ausmash_lib.get_player(region, player)['ID']
	except HTTPError:
		return template('character_matchups_error', region=region, name=player)
	
	scores = ausmash_lib.group_player_score_against_characters(player_id, game)
	return template('character_matchups_results', region=region, player=player, game=game, scores=scores)

run(app, host='0.0.0.0', port=os.environ.get('PORT', 5000))
