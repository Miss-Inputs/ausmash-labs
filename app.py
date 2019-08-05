import os
from urllib.request import HTTPError

from bottle import Bottle, run, request, template, static_file

import ausmash_lib
import ausmash_api

app = Bottle()

@app.route('/')
def index():
	return template('main_page')

@app.route('/js/<filename:path>')
def static_js(filename):
	return static_file(filename, root='./js')

@app.route('/event_elo/main')
def elo_change_from_event():
	#I should use IDs...
	regions = {region['Short']: region['Name'] for region in ausmash_api.get_regions()}
	games = {game['Short']: game['Name'] for game in ausmash_api.get_games()}
	return template('elo_change_from_event_main', regions=regions, games=games)

@app.route('/event_elo/results')
def elo_change_from_event_results():
	#Heck you pylint… query['blah'] results in an error too
	region = request.query.region #pylint: disable=no-member
	player = request.query.player #pylint: disable=no-member
	game = request.query.game #pylint: disable=no-member
	
	try:
		player_id = ausmash_api.get_player(region, player)['ID']
	except HTTPError:
		return template('character_matchups_error', region=region, name=player)
	
	result_summary = ausmash_lib.summarize_player_events(player_id, game)
	return template('elo_change_from_event_results', region=region, player=player, game=game, result_summary=result_summary)

@app.route('/character_matchups/main')
def character_matchups():
	#I should use IDs...
	regions = {region['Short']: region['Name'] for region in ausmash_api.get_regions()}
	games = {game['Short']: game['Name'] for game in ausmash_api.get_games()}
	return template('character_matchups_main', regions=regions, games=games)

@app.route('/character_matchups/results')
def character_matchup_results():
	region = request.query.region #pylint: disable=no-member
	player = request.query.player #pylint: disable=no-member
	game = request.query.game #pylint: disable=no-member
	
	try:
		player_id = ausmash_api.get_player(region, player)['ID']
	except HTTPError:
		return template('character_matchups_error', region=region, name=player)
	
	scores = ausmash_lib.group_player_score_against_characters(player_id, game)
	return template('character_matchups_results', region=region, player=player, game=game, scores=scores)

run(app, host='0.0.0.0', port=os.environ.get('PORT', 5000))
