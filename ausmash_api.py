#!/usr/bin/env python3

import json
import os
from functools import lru_cache
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote

api_key = os.environ['API_KEY']

endpoint = 'https://api.ausmash.com.au'

def get_request(url):
	return Request(url, headers={'X-ApiKey': api_key})

@lru_cache(maxsize=None)
def get_regions():
	url = endpoint + '/regions'
	with urlopen(get_request(url)) as r:
		return json.load(r)
		
@lru_cache(maxsize=None)
def get_games():
	url = endpoint + '/games'
	with urlopen(get_request(url)) as r:
		return json.load(r)
		
def get_characters(game_shortname):
	url = endpoint + '/characters'
	with urlopen(get_request(url)) as r:
		return [character for character in json.load(r) if character['GameShort'] == game_shortname]

def get_player(region, name):
	url = endpoint + '/players/find/{0}/{1}'.format(quote(name), region)
	with urlopen(get_request(url)) as r:
		return json.load(r)
		
def get_player_matches(player_id, start_date=None, end_date=None):
	url = endpoint + '/players/{0}/matches'.format(player_id)
	params = {}
	if start_date:
		params['startDate'] = start_date
	if end_date:
		params['endDate'] = end_date
	if params:
		url += '?' + urlencode(params)

	with urlopen(get_request(url)) as r:
		return json.load(r)

def get_player_event_results(player_id, start_date=None, end_date=None):
	url = endpoint + '/players/{0}/results'.format(player_id)
	params = {}
	if start_date:
		params['startDate'] = start_date
	if end_date:
		params['endDate'] = end_date
	if params:
		url += '?' + urlencode(params)

	with urlopen(get_request(url)) as r:
		return json.load(r)

def get_event_results(event_id):
	url = endpoint + '/events/{0}/results'.format(event_id)
	with urlopen(get_request(url)) as r:
		return json.load(r)
