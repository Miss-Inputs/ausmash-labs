#!/usr/bin/env python3

import json
import math
import os
from urllib.request import Request, urlopen

api_key = os.environ['API_KEY']

endpoint = 'https://api.ausmash.com.au'

def get_request(url):
	return Request(url, headers={'X-ApiKey': api_key})

def get_player(region, name):
	url = endpoint + '/players/find/{0}/{1}'.format(name, region)
	with urlopen(get_request(url)) as r:
		return json.load(r)
		
def get_player_matches(region, name):
	player = get_player(region, name)
	url = endpoint + '/players/{0}/matches'.format(player['ID'])
	with urlopen(get_request(url)) as r:
		return json.load(r)
		
def get_player_matches_for_game(region, name, game_shortname):
	matches = get_player_matches(region, name)
	if not matches:
		return []
	for match in matches:
		if match['Event']['Game']['Short'] != game_shortname:
			continue
		yield match
			
def get_player_results_against_characters(region, name, game_shortname):
	player = get_player(region, name)
	
	results = {}
	matches = get_player_matches_for_game(region, name, game_shortname)
	for match in matches:
		if match['Winner'] is None:
			#Player just lost to someone who isn't in the database
			#This means they are the loser though, because if not, the match wouldn't be returned from get_player_matches_for_game
			is_winner = False
		else:
			is_winner = match['Winner']['ID'] == player['ID']
		opponent_characters = match['LoserCharacters'] if is_winner else match['WinnerCharacters']
		for opponent_char in opponent_characters:
			char_id = opponent_char['ID']
			if char_id not in results:
				results[char_id] = {'Wins': 0, 'Losses': 0}
			
			results[char_id]['Wins' if is_winner else 'Losses'] += 1
	return results
	
def get_characters(game_shortname):
	url = endpoint + '/characters'
	with urlopen(get_request(url)) as r:
		return [character for character in json.load(r) if character['GameShort'] == game_shortname]
	
def get_player_score_against_characters(region, name, game_shortname):
	results = get_player_results_against_characters(region, name, game_shortname)
	characters = get_characters(game_shortname)
	
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
	
def group_player_score_against_characters(region, name, game_shortname):
	scores = get_player_score_against_characters(region, name, game_shortname)
	
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
	