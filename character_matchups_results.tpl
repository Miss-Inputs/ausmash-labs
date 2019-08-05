<html>
	<head>
		<title>Ausmash: Results against each character</title>
	</head>
	<body>
		<h1>Scores vs. each character in {{game}} for {{player}} from {{region}}</h1>
		<table>
		%for group, char_list in scores.items():
			%#<h2>{{group}}</h2>
			%#{{', '.join(char_list)}}<br />
			<tr>
				<td>{{group}}</td>
				%#TODO: Get images from somewhere
				<td>{{', '.join(char_list)}}</td>
			</tr>
		%end
		</table>
	</body>
</html>