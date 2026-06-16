import os
import redis

# Connects to the Redis server
client = redis.Redis.from_url(
    os.environ["REDIS_URI"],
    decode_responses=True
)