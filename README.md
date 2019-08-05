# ausmash-opponent-matchups
Ausmash API: Player vs character matchups

This is a little thing that uses data from Ausmash to display matchups against each character that a player has in a given Smash game: which characters they lose to, which characters they don't, and also who hasn't been played against entirely. Perhaps it may be of use to you.

Of course, the results can only be as accurate as the character data uploaded to the site by users; if that doesn't get updated then this won't work. So if the results make you say "hmm hang on that doesn't seem right", that's probably why. 

This is the source of that website, with all the Heroku thingoes to make it do something; in theory all that would be needed to run it yourself (if you for some reason wanted to do that) would have an environment variable API_KEY with your Ausmash API key (or you could hardcode it in ausmash_lib.py but that's probably a bad idea).

ausmash_lib.py contains the actual fun stuff, app.py contains the extremely lazy and quick and dirty web page in front of it.
