
import db
from pymemcache.client.base import Client

cache = Client('memcached')


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
	