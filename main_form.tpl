<html>
	<head>
		<title>Ausmash: Results against each character</title>
	</head>
	<body>
		<form action="/main" method="get">
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
	</body>
</html>