import os

from bottle import Bottle, run, request, template

import ausmash_lib

app = Bottle()

@app.route('/')
def index():
	main_form = """
	<html>
		<head>
			<title>Ausmash: Results against each character</title>
		</head>
		<body>
			<form action="/main" method="get">
				Region: <input name="region" type="text"><br />
				Player name: <input name="player" type="text"><br />
				Game shortname: <input name="game" type="text"><br />
				<input value="Submit" type="submit" />
			</form>
		</body>
	</html>
	"""
	return main_form

@app.route('/main')
def get_stuff():
	region = request.query.region
	player = request.query.player
	game = request.query.game
	scores = ausmash_lib.group_player_score_against_characters(region, player, game)
	return template('scores_view', region=region, player=player, game=game, scores=scores)

run(app, host='0.0.0.0', port=os.environ.get('PORT', 5000))