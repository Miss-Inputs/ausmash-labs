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
		row['Entrants'] = len(ausmash_api.get_event_results(event_id)) #This seems inefficient and I'm not sure if there would be a better way to do this…

		wins, losses = count_wins_losses(matches[event_id], player_id)
		row['Score'] = (wins, losses)
		elo_change = get_elo_change_from_matches(matches[event_id], player_id)
		row['Elo change'] = elo_change

		rows.append(row)

	return rows
		
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
				results[char_id] = {'Wins': 0, 'Losses': 0}
			
			results[char_id]['Wins' if is_winner else 'Losses'] += 1
	return results
	
def get_player_score_against_characters(player_id, game_shortname):
	results = get_player_results_against_characters(player_id, game_shortname)
	characters = ausmash_api.get_characters(game_shortname)
	
	scores = {}
	for character in characters:
		if character['ID'] not in results:
			scores[character['Name']] = None
		else:
			char_results = results[character['ID']]
			if char_results['Losses'] == 0:
				scores[character['Name']] = math.inf
			else:
				scores[character['Name']] = char_results['Wins'] / char_results['Losses']
	return scores
	
def group_player_score_against_characters(player_id, game_shortname):
	scores = get_player_score_against_characters(player_id, game_shortname)
	
	groups = {
		'Always win': [],
		'Mostly win': [],
		'Neutral': [],
		'Mostly lose': [],
		'Never won': [],
		'Never played': [],
	}
	for character, score in sorted(scores.items(), key=lambda t: -1 if t[1] is None else t[1]):
		if score is None:
			groups['Never played'].append(character)
		elif score == 0:
			groups['Never won'].append(character)
		elif score == 1:
			groups['Neutral'].append(character)
		elif score == math.inf:
			groups['Always win'].append(character)
		elif score < 1:
			groups['Mostly lose'].append(character)
		elif score > 1:
			groups['Mostly win'].append(character)
	return groups
