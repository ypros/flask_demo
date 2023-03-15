
import db
import pylibmc


cache = pylibmc.Client(['127.0.0.1:11211'])

def get_feed_chached(user_id):
	feed = cache.get(user_id)
	if feed is None:
		result = db.get_feed(user_id)

		if result is not None:
			cache.set('user_id', result)

		return result

	else:
		return feed	

def clear_cache(user_id):
	cache.delete(user_id)
	