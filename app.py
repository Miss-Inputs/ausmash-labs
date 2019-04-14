import os

from bottle import Bottle, run, request

import the_actual_fucking_thing

app = Bottle()

@app.route('/')
def index():
	main_form = """
	<html>
		<head>
			<title>meow</title>
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
#@app.route('/main/<region>/<player>/<game>')
def get_stuff():
	region = request.query.region
	player = request.query.player
	game = request.query.game
	scores = the_actual_fucking_thing.group_player_score_against_characters(region, player, game)
	return scores

run(app, host='0.0.0.0', port=os.environ.get('PORT', 5000))