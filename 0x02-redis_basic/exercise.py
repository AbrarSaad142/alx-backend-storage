#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, 
store an instance of the Redis client as a private variable named _redis
 (using redis.Redis()) and flush the instance using flushdb.
"""


from typing import Union
import uuid

import redis


class Cache:
    def __init__(self):
        """
        Initialize the Cache instance.
        """
        self._redis = redis.Redis()  # Create an instance of Redis client
        self._redis.flushdb()  # Flush the database

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): Data to be stored in Redis.

        Returns:
            str: The key under which the data was stored.
        """
        # Generate a random key
        random_key = str(uuid.uuid4())

        # Store the data in Redis using the generated key
        self._redis.set(random_key, data)

        # Return the key
        return random_key
