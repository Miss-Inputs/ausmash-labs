<html>
	<head>
		<title>Ausmash: Elo change from events</title>
		<style>
			th, td {
				border-width: 1px;
				border-style: solid;
			}
			tr.redemption {
				background-color: #dddddd;
			}
		</style>
		<script src="/js/sorttable.js"></script>
	</head>
	<body>
		<h1>Elo change for each event in {{game}} for {{player}} from {{region}}</h1>
		<table class='sortable'>
			<tr>
				<th>Tourney</th>
				<th>Date</th>
				<th>Event</th>
				<th>Placing</th>
				<th>Score</th>
				<th>Elo change</th>
				<th>Tourney Elo change</th>
			</tr>

		%for row in sorted(result_summary, key=lambda row: row['Elo change'], reverse=True):
			%event_name_lower = row['Event'].lower()
			<tr{{!' class="redemption"' if ('redemption' in event_name_lower or 'amateur' in event_name_lower or 'ammies' in event_name_lower) else ''}}>
				<td>{{row['Tourney']}}</td>
				<td>{{row['Date']}}</td>
				<td>{{row['Event']}}</td>
				%#<td>{{'{0}/{1}'.format(row['Placing'], row['Entrants'])}}</td>
				<td>{{row['Placing']}}</td>
				<td>{{'{0}-{1}'.format(*row['Score'])}}</td>
				<td>{{row['Elo change']}}</td>
				<td>{{tourney_elo_changes.get(row['Tourney'])}}</td>
			</tr>
		%end
		</table>
		<p>
			<a href='/event_elo/main'>Go back</a>
			<a href='/'>Go back home</a>
		</p>
	</body>
</html>