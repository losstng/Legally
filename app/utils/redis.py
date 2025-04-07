import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"), #where the server is located
    port=int(os.getenv("REDIS_PORT", 6379)), #which way and encryption to access this server
    db=0, #redis has 16 different db by default, and we are using the number 0
    decode_responses=True #since redis communicate in bytes, it will self decode for us to UTF-8
)