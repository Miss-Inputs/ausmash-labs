%import math
<html>
	<head>
		<title>Ausmash: Win rates against each character</title>
		<style>
			.sortable th, .sortable td {
				border-width: 1px;
				border-style: solid;
			}
		</style>
		<script src="/js/sorttable.js"></script>
	</head>
	<body>
		<h1>Win rates against each character in {{game}} for {{player}} from {{region}}</h1>
		<table>
		%for group, char_list in summary.items():
			<tr>
				<td>{{group}}</td>
				%#I want to have images here one day but they'd probably have to be hosted locally and then I just can't be bothered adding them all I guess
				<td>{{', '.join(char_list)}}</td>
			</tr>
		%end
		</table>
		<table class='sortable'>
			<tr>
				<th>Character</th>
				<th>Wins</th>
				<th>Losses</th>
				<th>Total</th>
				<th>Win%</th>
				%#<th>Win/Loss Ratio</th>
				<th>Win/Loss Difference</th>
				<th>Elo gain</th>
				<th>Elo loss</th>
				<th>Elo change</th>
				<th>Avg Elo change per match</th>
			</tr>
		<%
			def format_float(f):
				return str(int(f) if float(f).is_integer() else round(f, 2))
			end
		%>

		%for name, row in matchups.items():
			<tr>
				<td>{{name}}</td>
				<td>{{format_float(row['Wins'])}}</td>
				<td>{{format_float(row['Losses'])}}</td>
				%total = row['Wins'] + row['Losses']
				<td>{{format_float(total)}}</td>
				%if total == 0:
					<td sorttable_customkey="-1">Never played</td>
				%else:
					<td>{{'{0:.0%}'.format(row['Wins'] / total)}}</td>
				%end
				<td>{{format_float(row['Wins'] - row['Losses'])}}</td>
				<td>{{row['Elo gain']}}</td>
				<td>{{row['Elo loss']}}</td>
				%elo_change = row['Elo gain'] - row['Elo loss']
				<td>{{elo_change}}</td>
				<td>{{round(elo_change / total, 2) if total != 0 else 'N/A'}}</td>
			</tr>
		%end
		</table>
		<p>
			<a href='/character_matchups/main'>Go back</a>
			<a href='/'>Go back home</a>
		</p>
	</body>
</html>