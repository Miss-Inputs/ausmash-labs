<html>
	<head>
		<title>Ausmash: Results against each character</title>
	</head>
	<body>
		<p>
			This is a little thing that uses Ausmash character data to display matchups against each character that a player has in a given Smash game: which characters they lose to, which characters they don't, and also who hasn't been played against entirely. Perhaps it may be of use to you.
		</p>
		<p>
			Of course, the results can only be as accurate as the character data uploaded to the site by users; if that doesn't get updated then this won't work. So if the results make you say "hmm hang on that doesn't seem right", that's probably why.
		</p>
		<p>
			If you get a Heroku application error this is because I suck and it's timing out, but if you refresh it then it should probably work that time, so don't panic.
		</p>
		<form action="/character_matchups/results" method="get">
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
			<input type="checkbox" name="combine_echoes" checked="checked" id="combineEchoes" />
			<label for="combineEchoes">Combine echo fighters that are basically equivalent (Peach/Daisy, etc)</label><br />
			<label for="minimumDate">Only consider matches that happened on or after this date (or leave blank):</label>
			<input type="date" name="minimum_date" id="minimumDate"/><br />
			<input type="checkbox" name="exclude_low_level" id="excludeLowLevel" />
			<label for="excludeLowLevel">Exclude matches against players with less than or equal to 1000 Elo</label><br />
			<input type="checkbox" name="partial_usage" id="partialUsage" checked="checked"/>
			<label for="partialUsage">If multiple characters are used in a set, count each as a fraction of a usage</label><br />
			<input value="Submit" type="submit" />
		</form>
		<p>
			<a href='/'>Go back home</a>
		</p>
	</body>
</html>