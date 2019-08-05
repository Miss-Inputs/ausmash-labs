#!/usr/bin/env python3

import json
import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode

api_key = os.environ['API_KEY']

endpoint = 'https://api.ausmash.com.au'

def get_request(url):
	return Request(url, headers={'X-ApiKey': api_key})

def get_regions():
	url = endpoint + '/regions'
	with urlopen(get_request(url)) as r:
		return json.load(r)
		
def get_games():
	url = endpoint + '/games'
	with urlopen(get_request(url)) as r:
		return json.load(r)
		
def get_characters(game_shortname):
	url = endpoint + '/characters'
	with urlopen(get_request(url)) as r:
		return [character for character in json.load(r) if character['GameShort'] == game_shortname]

def get_player(region, name):
	url = endpoint + '/players/find/{0}/{1}'.format(name, region)
	with urlopen(get_request(url)) as r:
		return json.load(r)
		
def get_player_matches(player_id, start_date=None, end_date=None):
	url = endpoint + '/players/{0}/matches'.format(player_id)
	if start_date is not None or end_date is not None:
		url += '?' + urlencode({'start_date': start_date, 'end_date': end_date})

	with urlopen(get_request(url)) as r:
		return json.load(r)

def get_player_event_results(player_id, start_date=None, end_date=None):
	url = endpoint + '/players/{0}/results'.format(player_id)
	if start_date is not None or end_date is not None:
		url += '?' + urlencode({'start_date': start_date, 'end_date': end_date})

	with urlopen(get_request(url)) as r:
		return json.load(r)

def get_event_results(event_id):
	url = endpoint + '/events/{0}/results'.format(event_id)
	with urlopen(get_request(url)) as r:
		return json.load(r)
