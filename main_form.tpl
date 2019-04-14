<html>
	<head>
		<title>Ausmash: Results against each character</title>
	</head>
	<body>
		<p>
			This is a little thing that uses data from <a href="https://ausmash.com.au/">Ausmash</a> to display matchups against each character that a player has in a given Smash game: which characters they lose to, which characters they don't, and also who hasn't been played against entirely. Perhaps it may be of use to you.
		</p>
		<p>
			Of course, the results can only be as accurate as the character data uploaded to the site by users; if that doesn't get updated then this won't work. So if the results make you say "hmm hang on that doesn't seem right", that's probably why.
		</p>
		<p>
			This was made by <a href="https://twitter.com/Zowayix">Megan Leet</a> in the span of several hours. Source is available on <a href="https://github.com/Zowayix/ausmash-opponent-matchups">GitHub</a>, and I realise at this point that I've failed to come up with a consistent name for this thing.
		</p>
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