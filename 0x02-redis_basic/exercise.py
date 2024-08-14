import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with counting functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count and then calls the original method.
        """
        # Generate the key using the qualified name of the method
        key = method.__qualname__

        # Increment the count in Redis
        self._redis.incr(key)

        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper

class Cache:
    def __init__(self):
        """
        Initialize the Cache instance.
        """
        self._redis = redis.Redis()  # Create an instance of Redis client
        self._redis.flushdb()  # Flush the database

    @count_calls
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

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, None]:
        """
        Retrieve data from Redis and optionally apply a conversion function.

        Args:
            key (str): The key to retrieve the data.
            fn (Optional[Callable]): A callable used to convert the data back to the desired format.

        Returns:
            Union[str, bytes, int, None]: The retrieved data, optionally converted using the provided callable.
        """
        # Retrieve the data from Redis
        data = self._redis.get(key)
        
        if data is None:
            return None  # Return None if the key does not exist
        
        if fn:
            return fn(data)  # Apply the conversion function if provided
        
        return data  # Return the data as-is if no function is provided

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data from Redis and convert it to a string using UTF-8 decoding.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Optional[str]: The data as a UTF-8 decoded string, or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data from Redis and convert it to an integer.

        Args:
            key (str): The key to retrieve the data.

        Returns:
            Optional[int]: The data converted to an integer, or None if the key does not exist.
        """
        return self.get(key, int)
