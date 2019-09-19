#!/usr/bin/env python3

import math

import ausmash_api

def get_player_matches_in_multiple_events(player_id, event_ids):
	all_matches = ausmash_api.get_player_matches(player_id)

	matches = {}
	for event_id in event_ids:
		event_matches = [match for match in all_matches if match['Event']['ID'] == event_id]
		matches[event_id] = event_matches
	return matches

def get_player_matches_in_event(player_id, event_id, tourney_date=None):
	#Seems for multi-day events (majors), Ausmash acts as though everything happens on the last day, so no edge case to worry about there
	if tourney_date:
		matches = ausmash_api.get_player_matches(player_id, tourney_date, tourney_date)
	else:
		matches = ausmash_api.get_player_matches(player_id)

	if not matches:
		return []
	for match in matches:
		if match['Event']['ID'] != event_id:
			continue
		yield match
	return []

def get_elo_change_from_matches(matches, player_id):
	total = 0
	for match in matches:
		change = match['EloMovement']
		if change is None:
			#Tournament is too recent, Elo for this week hasn't been processed yet
			continue

		if match['Winner'] is None:
			#Player just lost to someone who isn't in the database
			is_winner = False
		else:
			is_winner = match['Winner']['ID'] == player_id

		if is_winner:
			total += change
		else:
			total -= change
	return total

def count_wins_losses(matches, player_id):
	wins = 0
	losses = 0
	for match in matches:
		if match['Winner'] is None:
			#Player just lost to someone who isn't in the database
			is_winner = False
		else:
			is_winner = match['Winner']['ID'] == player_id

		if is_winner:
			wins += 1
		else:
			losses += 1
	return wins, losses	

def summarize_player_events(player_id, game):
	results = [result for result in ausmash_api.get_player_event_results(player_id) if result['Event']['Game']['Short'] == game]
	rows = []
	event_ids = [result['Event']['ID'] for result in results]
	matches = get_player_matches_in_multiple_events(player_id, event_ids)

	for result in results:
		row = {}
		row['Tourney'] = result['Tourney']['Name']
		row['Date'] = result['Tourney']['TourneyDate']
		row['Event'] = result['Event']['Name']
		row['Placing'] = result['Result']
		event_id = result['Event']['ID']

		#row['Entrants'] = len(ausmash_api.get_event_results(event_id)) #This seems inefficient and I'm not sure if there would be a better way to do this…
		#Yeah nah that's way too slow kiddo

		wins, losses = count_wins_losses(matches[event_id], player_id)
		row['Score'] = (wins, losses)
		elo_change = get_elo_change_from_matches(matches[event_id], player_id)
		row['Elo change'] = elo_change

		rows.append(row)

	return rows

def get_tourney_elo_changes(result_summary):
	results = {}
	for row in result_summary:
		if row['Tourney'] not in results:
			results[row['Tourney']] = 0
		results[row['Tourney']] += row['Elo change']
	return results
		
def get_player_matches_for_game(player_id, game_shortname):
	matches = ausmash_api.get_player_matches(player_id)
	if not matches:
		return []
	for match in matches:
		if match['Event']['Game']['Short'] != game_shortname:
			continue
		yield match
	return []
			
def get_player_results_against_characters(player_id, game_shortname):
	results = {}
	matches = get_player_matches_for_game(player_id, game_shortname)
	for match in matches:
		if match['Winner'] is None:
			#Player just lost to someone who isn't in the database
			#This means they are the loser though, because if not, the match wouldn't be returned from get_player_matches_for_game
			is_winner = False
		else:
			is_winner = match['Winner']['ID'] == player_id
		opponent_characters = match['LoserCharacters'] if is_winner else match['WinnerCharacters']
		for opponent_char in opponent_characters:
			char_id = opponent_char['ID']
			if char_id not in results:
				results[char_id] = {'Wins': 0, 'Losses': 0, 'Elo gain': 0, 'Elo loss': 0}
			
			results[char_id]['Wins' if is_winner else 'Losses'] += 1
			if match['EloMovement'] is not None:
				results[char_id]['Elo gain' if is_winner else 'Elo loss'] += match['EloMovement']
	return results
	
equivalent_echo_fighters = {
	'Peach/Daisy': ('Peach', 'Daisy'),
	'Pits': ('Pit', 'Dark Pit'),
	'Samuses': ('Samus', 'Dark Samus'),
	'Belmonts': ('Simon', 'Richter'),
}

def get_player_matchups_against_characters(player_id, game_shortname, combine_echoes=False):
	results = get_player_results_against_characters(player_id, game_shortname)
	characters = ausmash_api.get_characters(game_shortname)
	
	matchups = {}
	for character in characters:
		name = character['Name']
		if combine_echoes:
			for combined, fighters in equivalent_echo_fighters.items():
				if name in fighters:
					name = combined
					break

		if name not in matchups:
			matchups[name] = {'Wins': 0, 'Losses': 0, 'Ratio': None, 'Elo gain': 0, 'Elo loss': 0}

		if character['ID'] in results:
			char_results = results[character['ID']]
			wins = char_results['Wins'] + matchups[name]['Wins']
			losses = char_results['Losses'] + matchups[name]['Losses']

			if losses == 0:
				#Never lost
				ratio = math.inf
			else:
				ratio = wins / losses
			elo_gain = char_results['Elo gain'] + matchups[name]['Elo gain']
			elo_loss = char_results['Elo loss'] + matchups[name]['Elo loss']
			matchups[name] = {'Wins': wins, 'Losses': losses, 'Ratio': ratio, 'Elo gain': elo_gain, 'Elo loss': elo_loss}
			
	return matchups

def group_player_character_matchups(matchups):	
	groups = {
		'Always win': [],
		'Mostly win': [],
		'Neutral': [],
		'Mostly lose': [],
		'Never won': [],
		'Never played': [],
	}
	for character, matchup in sorted(matchups.items(), key=lambda t: -1 if t[1]['Ratio'] is None else t[1]['Ratio']):
		ratio = matchup['Ratio']
		if ratio is None:
			groups['Never played'].append(character)
		elif ratio == 0:
			groups['Never won'].append(character)
		elif ratio == 1:
			groups['Neutral'].append(character)
		elif ratio == math.inf:
			groups['Always win'].append(character)
		elif ratio < 1:
			groups['Mostly lose'].append(character)
		elif ratio > 1:
			groups['Mostly win'].append(character)
	return groups
