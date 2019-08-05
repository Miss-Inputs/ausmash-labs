<html>
	<head>
		<title>Ausmash: Elo change from events</title>
		<style>
			th, td {
				border-width: 1px;
				border-style: solid;
			}
		</style>
	</head>
	<body>
		<h1>Elo change for each event in {{game}} for {{player}} from {{region}}</h1>
		<table>
			<tr>
				<th>Tourney</th>
				<th>Date</th>
				<th>Event</th>
				<th>Placing</th>
				<th>Score</th>
				<th>Elo change</th>
			</tr>

		%for row in sorted(result_summary, key=lambda row: row['Elo change'], reverse=True):
			<tr>
				<td>{{row['Tourney']}}</td>
				<td>{{row['Date']}}</td>
				<td>{{row['Event']}}</td>
				%#<td>{{'{0}/{1}'.format(row['Placing'], row['Entrants'])}}</td>
				<td>{{row['Placing']}}</td>
				<td>{{'{0}-{1}'.format(*row['Score'])}}</td>
				<td>{{row['Elo change']}}</td>
			</tr>
		%end
		</table>
	</body>
</html>