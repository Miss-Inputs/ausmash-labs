<html>
	<head>
		<title>Ausmash: Elo change from events</title>
	</head>
	<body>
		<p>
			Summarizes results for a player / game by adding up all the Elo movement for that player for each event, which may or may not give interesting insight into tournament performance.
		</p>
		<form action="/event_elo/results" method="get">
			Region: <select name="region">
			%for region_short, region_name in regions.items():
				<option value="{{region_short}}">{{region_name}}</option>
			%end
			</select>
			<br />
			Player name: <input name="player" type="text"><br />
			Game: <select name="game">
			%for game_short, game_name in games.items():
				<option value="{{game_short}}">{{game_name}}</option>
			%end
			</select>
			<br />
			<input value="Submit" type="submit" />
		</form>
		<p>
			<a href='/'>Go back home</a>
		</p>
	</body>
</html>